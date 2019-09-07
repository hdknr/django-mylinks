from django.contrib import admin
from .. import models
from . import forms, inlines


@admin.register(models.Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['id', 'host', 'name', ]


@admin.register(models.Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'url', 'site', 'subclass_type']
    list_filter = ['subclass_type']
    raw_id_fields = ['site', 'content']
    search_fields = ['title', 'url', ]
    readonly_fields = ['markdown', 'embed_html']
    form = forms.LinkForm
    inlines = [
        inlines.LinkTagItemInline,
    ]


@admin.register(models.Embed)
class EmbedAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'url', 'site']
    raw_id_fields = ['site', 'content']
    exclude = ['created_at', 'subclass_type']
    search_fields = ['title', 'url', ]
    readonly_fields = ['markdown', 'html', 'data', 'source']
    inlines = [
        inlines.LinkTagItemInline,
    ]
