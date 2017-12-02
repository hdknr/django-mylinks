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
        fields = '__all__'
        read_only_fields = ['site', 'embed', 'source']
