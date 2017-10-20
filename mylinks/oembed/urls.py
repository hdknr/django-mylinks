from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<content_type>[^/]+)(?:/(?P<style>[^/]+))?/(?P<id>\d+)$',
        views.api, name="mylinks_oembed_api"),
    url(r'^(?P<content_type>[^/]+)(?:/(?P<style>[^/]+))?/(?P<id>\d+)/embed$',
        views.embed, name="mylinks_oembed_embed"),
    url(r'^(?P<content_type>[^/]+)(?:/(?P<style>[^/]+))?/(?P<id>\d+)/widget$',  # NOQA
        views.widget, name="mylinks_oembed_widget"),
    url(r'^(?P<content_type>[^/]+)(?:/(?P<style>[^/]+))?/(?P<id>\d+)/widget.js',   # NOQA
        views.script, name="mylinks_oembed_script"),
]
