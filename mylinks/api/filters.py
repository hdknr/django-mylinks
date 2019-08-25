import django_filters
from .. import models


class PageFilter(django_filters.FilterSet):

    class Meta:
        model = models.Page
        exclude = []


class LinkFilter(django_filters.FilterSet):

    class Meta:
        model = models.Link
        exclude = []
