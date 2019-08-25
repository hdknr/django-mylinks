from django.utils.decorators import available_attrs
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django import http
from functools import wraps


def contenttype_instance(content_type_key, id):
    app_label, model = content_type_key.split('.')
    ct = ContentType.objects.get_by_natural_key(app_label, model)
    return ct and ct.get_object_for_this_type(id=id)


def oembed(**params):

    def _decorator(view_func):

        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapper(request, content_type, style, id, instance=None, **kwargs):
            style = style or 'default'
            instance = instance or contenttype_instance(content_type, id)
            if not instance:
                raise http.Http404
            response = view_func(request, content_type, style, id, instance=instance)
            return response

        return _wrapper

    return _decorator
