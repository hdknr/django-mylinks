from django.contrib.contenttypes.models import ContentType
from django.template.loader import get_template
from django import http
from django.template.response import TemplateResponse
from . import responses
#
import json
from logging import getLogger
logger = getLogger()


def contenttype_instance(content_type_key, id):
    app_label, model = content_type_key.split('.')
    ct = ContentType.objects.get_by_natural_key(app_label, model)
    return ct and ct.get_object_for_this_type(id=id)


def get_instance(content_type_key, id):
    return contenttype_instance(content_type_key, id)


def api(request, content_type, style, id):
    ''' oembed api: return JSON for the following link@rel

    <link rel="alternate" type="application/json+oembed"
     href="{% url 'mylinks_oembed_api'
        content_type='blogs.article' id=instance.id %}" >

    '''
    style = style or 'default'
    instance = get_instance(content_type, id)
    if not instance:
        return responses.page_not_found()

    template = f"mylinks/oembed/{content_type}/{style}/oembed.json"
    src = get_template(template).render(
        context=dict(request=request, content_type=content_type, instance=instance))
    default = json.loads(src)

    # HTML includes link to 'embed' javascipt
    embed_html = f"mylinks/oembed/{content_type}/{style}/embed.html"
    res = embed(request, content_type, style, id)
    default['html'] = res.rendered_content
    
    return responses.cors(responses.JSONResponse(default), origin='*')


def embed(request, content_type, style, id):
    style = style or 'default'
    instance = get_instance(content_type, id)
    if not instance:
        return responses.page_not_found()

    template = f"mylinks/oembed/{content_type}/{style}/embed.html"
    context=dict(request=request, instance=instance, content_type=content_type)
    res = TemplateResponse(request, template, context=context)
    return responses.cors(res, origin='*')


def script(request, content_type, style, id):
    ''' Javascript to fetch iframe widget and render in browser
    '''
    style = style or 'default'
    instance = get_instance(content_type, id)
    if not instance:
        return responses.page_not_found()

    template = f"mylinks/oembed/{content_type}/{style}/widget.js"
    context=dict(request=request, instance=instance, content_type=content_type)

    res = TemplateResponse(
        request, template, 
        context=context,
        content_type='application/javascript')

    return responses.cors(res, origin='*')


def widget(request, content_type, style, id):
    style = style or 'default'
    instance = get_instance(content_type, id)
    if not instance:
        return response.page_not_found()

    template = f"mylinks/oembed/{content_type}/{style}/widget.html"

    res = TemplateResponse(
        request, template, 
        context=dict(request=request, instance=instance))

    return responses.cors(res, origin='*')

