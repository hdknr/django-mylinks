from django import template
from django.urls import reverse
from django.contrib.sites.models import Site

register = template.Library()


@register.simple_tag(takes_context=True)
def buildfullurl(context, path):
    if 'request' in context:
        return context['request'].build_absolute_uri(path)
    site = Site.objects.get_current()
    if not site:
        return path
    return f"//{site.domain}{path}"



@register.simple_tag(takes_context=True)
def fullurl(context, name, *args, **kwargs):
    return buildfullurl(context, reverse(name, args=args, kwargs=kwargs))
