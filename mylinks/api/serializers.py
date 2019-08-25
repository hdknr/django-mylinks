from rest_framework import serializers, fields
from django.forms.models import model_to_dict
from .. import models


class SiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Site
        fields = '__all__'


class PageSerializer(serializers.ModelSerializer):
    site = SiteSerializer(read_only=True)

    class Meta:
        model = models.Page
        exclude = ['source']
        read_only_fields = ['site', 'embed', ]

    def is_valid(self, *args, **kwargs):
        res = super(PageSerializer, self).is_valid(*args, **kwargs)
        if not res:
            self._existing_instance = self.Meta.model.objects.filter(
                    url=self.initial_data.get('url', '')).first()
            res = self._existing_instance and True or False
        return res

    def save(self, **kwargs):
        if hasattr(self, '_existing_instance'):
            self.instance = self._existing_instance
            return self.instance
        return super(PageSerializer, self).save(**kwargs)


class LinkSerializer(serializers.ModelSerializer):
    site = SiteSerializer(read_only=True)

    class Meta:
        model = models.Link
        fields = '__all__'
        read_only_fields = ['site', ]

    def run_validation(self, data=fields.empty):
        self._existing_instance = ('url' in data) \
            and models.Link.objects.filter(url=data['url']).first()
        return model_to_dict(self._existing_instance) \
            or super(LinkSerializer, self).run_validation(data=data)

    def save(self, **kwargs):
        if hasattr(self, '_existing_instance'):
            self.instance = self._existing_instance
            return self.instance
        return super(LinkSerializer, self).save(**kwargs)
