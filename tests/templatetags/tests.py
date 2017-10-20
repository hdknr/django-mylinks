# -*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse
register = template.Library()


@register.simple_tag(takes_context=True)
def fullurl(context, name, *args, **kwargs):
    url = reverse(name, args=args, kwargs=kwargs)
    return context['request'].build_absolute_uri(url)


@register.simple_tag(takes_context=True)
def buildfullurl(context, path):
    return context['request'].build_absolute_uri(path)
