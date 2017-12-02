from django.contrib.contenttypes.models import ContentType
from django.template.loader import get_template
from django import http
from django.template.response import TemplateResponse
from mylinks import responses
#
from logging import getLogger
import json
logger = getLogger()


def contenttype_instance(content_type_key, id):
    app_label, model = content_type_key.split('.')
    ct = ContentType.objects.get_by_natural_key(app_label, model)
    return ct and ct.get_object_for_this_type(id=id)


def get_instance(content_type_key, id):
    return contenttype_instance(content_type_key, id)


def api(request, content_type, style, id):
    '''
    <link rel="alternate" type="application/json+oembed"
     href="{% fullurl 'corekit_oembed_api'
        content_type='blogs.article' id=instance.id %}" >
    '''
    style = style or 'default'
    instance = get_instance(content_type, id)
    if not instance:
        return responses.page_not_found()

    template = "mylinks/oembed/{}/{}/oembed.json".format(content_type, style)
    src = get_template(template).render(
        context=dict(request=request, instance=instance))
    default = json.loads(src)
    embed_html = "mylinks/oembed/{}/{}/embed.html".format(content_type, style)
    default['html'] = get_template(embed_html).render(
        context=dict(request=request, instance=instance))

    return responses.cors(responses.JSONResponse(default), origin='*')


def embed(request, content_type, style, id):
    style = style or 'default'
    instance = get_instance(content_type, id)
    if not instance:
        return responses.page_not_found()

    template = "mylinks/oembed/{}/{}/embed.html".format(content_type, style)
    res = TemplateResponse(
        request, template, context=dict(request=request, instance=instance))
    return responses.cors(res, origin='*')


def widget(request, content_type, style, id):
    style = style or 'default'
    instance = get_instance(content_type, id)
    if not instance:
        return response.page_not_found()

    template = "mylinks/oembed/{}/{}/widget.html".format(content_type, style)
    res = TemplateResponse(
        request, template, context=dict(request=request, instance=instance))
    return responses.cors(res, origin='*')


def script(request, content_type, style, id):
    style = style or 'default'
    instance = get_instance(content_type, id)
    if not instance:
        return responses.page_not_found()

    template = "mylinks/oembed/{}/{}/widget.js".format(content_type, style)
    res = TemplateResponse(
        request, template, context=dict(request=request, instance=instance))
    return responses.cors(res, origin='*')
