from django.contrib.contenttypes.models import ContentType
from collections import OrderedDict
from rest_framework import viewsets, pagination, permissions
from rest_framework.response import Response
from . import models, serializers, filters


class Pagination(pagination.PageNumberPagination):
    page_size = 16
    max_page_size = 16
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page_range', list(self.page.paginator.page_range)),
            ('current_page', self.page.number),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class PageViewSet(viewsets.ModelViewSet):

    queryset = models.Page.objects.all()
    serializer_class = serializers.PageSerializer
    filter_class = filters.PageFilter
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    pagination_class = Pagination
