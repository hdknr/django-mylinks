from django.urls import path, include


urlpatterns = [
    path(r'api/', include('mylinks.api.urls')),
]
