from rest_framework import serializers, fields
from django.forms.models import model_to_dict
from .. import models


class SiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Site
        fields = '__all__'


class ContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Content
        exclude = ['source', 'data']
        read_only_fields = ['embed', ]

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
