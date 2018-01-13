from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import viewsets

router = DefaultRouter()
router.register(r'page', viewsets.PageViewSet, base_name='page')
router.register(r'link', viewsets.LinkViewSet, base_name='link')

urlpatterns = [
    url(r'', include(router.urls)),
]
