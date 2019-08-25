# django-mylinks

- Link and oembed

## settings.py

~~~py
INSTALLED_APPS = [
    'rest_framework',
    'django_filters',
    'rest_framework_filters',
    ...
    'mylinks',
    ...
]
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework_filters.backends.RestFrameworkFilterBackend', ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}
~~~

## urls.py

~~~py
from django.urls import path, include

urlpatterns = [
    ...
    path('mylinks/', include('mylinks.urls'))
    ...
]
~~~
