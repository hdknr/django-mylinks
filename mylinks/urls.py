from django.urls import path, include


urlpatterns = [
    path(r'oembed/', include('mylinks.oembed.urls')),
    path(r'api/', include('mylinks.api.urls')),
]
