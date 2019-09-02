from django.contrib import admin
from .. import models


@admin.register(models.Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['id', 'host', 'name', ]


@admin.register(models.Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'url', 'site']
    raw_id_fields = ['site', 'content']
    search_fields = ['title', 'url', ]
    readonly_fields = ['embed_html']


@admin.register(models.Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['id', 'url', ]
