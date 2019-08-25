from django.template.loader import get_template
from django import http
from django.template.response import TemplateResponse
from . import responses, decorators
#
import json
from logging import getLogger
logger = getLogger()


@decorators.oembed()
def api(request, content_type, style, id, instance=None):
    ''' oembed api: return JSON for the following link@rel

    <link rel="alternate" type="application/json+oembed"
     href="{% url 'mylinks_oembed_api'
        content_type='blogs.article' id=instance.id %}" >

    '''
    template = f"mylinks/oembed/{content_type}/{style}/oembed.json"
    src = get_template(template).render(
        context=dict(request=request, content_type=content_type, instance=instance))
    default = json.loads(src)

    # HTML includes link to 'embed' javascipt
    embed_html = f"mylinks/oembed/{content_type}/{style}/embed.html"
    res = embed(request, content_type, style, id)
    default['html'] = res.rendered_content
    
    return responses.cors(responses.JSONResponse(default), origin='*')


@decorators.oembed()
def embed(request, content_type, style, id, instance=None):
    template = f"mylinks/oembed/{content_type}/{style}/embed.html"
    context=dict(request=request, instance=instance, content_type=content_type)
    res = TemplateResponse(request, template, context=context)
    return responses.cors(res, origin='*')


@decorators.oembed()
def script(request, content_type, style, id, instance=None):
    ''' Javascript to fetch iframe widget and render in browser
    '''
    template = f"mylinks/oembed/{content_type}/{style}/widget.js"
    context=dict(request=request, instance=instance, content_type=content_type)

    res = TemplateResponse(
        request, template, 
        context=context,
        content_type='application/javascript')

    return responses.cors(res, origin='*')


@decorators.oembed()
def widget(request, content_type, style, id, instance=None):
    template = f"mylinks/oembed/{content_type}/{style}/widget.html"

    res = TemplateResponse(
        request, template, 
        context=dict(request=request, instance=instance))

    return responses.cors(res, origin='*')
