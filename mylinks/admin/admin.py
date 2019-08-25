from django.contrib import admin
from .. import models


class PageAdminInline(admin.TabularInline):
    model = models.Page
    extra = 1


@admin.register(models.Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['id', 'host', 'name', ]


@admin.register(models.Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'url', 'site']
    raw_id_fields = ['site']
    search_fields = ['title', 'url', ]


@admin.register(models.Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'url', ]
    raw_id_fields = ['site']
    search_fields = ['title', 'url', 'embed', 'source']
    readonly_fields = ['embed_html']
