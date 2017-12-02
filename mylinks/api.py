from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import viewsets

router = DefaultRouter()
router.register(r'page', viewsets.PageViewSet, base_name='page')

urlpatterns = [
    url(r'', include(router.urls)),
]
