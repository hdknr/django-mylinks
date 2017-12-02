from django.conf.urls import url, include
from . import api

urlpatterns = [
    url(r'^api/', include(api)),
]
