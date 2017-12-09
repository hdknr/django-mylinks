from rest_framework import serializers
from . import models


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
