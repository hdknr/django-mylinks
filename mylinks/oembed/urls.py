from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^(?P<content_type>[^/]+)(?:/(?P<style>[^/]+))?/(?P<id>\d+)$',
        views.api, name="mylinks_oembed_api"),
    re_path(r'^(?P<content_type>[^/]+)(?:/(?P<style>[^/]+))?/(?P<id>\d+)/embed$',
        views.embed, name="mylinks_oembed_embed"),
    re_path(r'^(?P<content_type>[^/]+)(?:/(?P<style>[^/]+))?/(?P<id>\d+)/widget$',  # NOQA
        views.widget, name="mylinks_oembed_widget"),
    re_path(r'^(?P<content_type>[^/]+)(?:/(?P<style>[^/]+))?/(?P<id>\d+)/widget.js',   # NOQA
        views.script, name="mylinks_oembed_script"),
]
