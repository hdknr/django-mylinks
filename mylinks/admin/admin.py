from django.contrib import admin
from django.urls import path
from .. import models
from . import forms, inlines, views


@admin.register(models.Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['id', 'host', 'name', ]


@admin.register(models.Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'url', 'site', 'subclass_type']
    list_filter = ['subclass_type']
    exclude = ['created_at']
    raw_id_fields = ['site', ]
    search_fields = ['title', 'url', ]
    readonly_fields = ['markdown', 'embed_html', 'site', 'subclass_type', 'updated_at', 'visited_at']
    inlines = [
        inlines.LinkTagItemInline,
    ]

    def get_urls(self):
        # https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_urls
        urls = [
            path('add/entry/', views.add_entry, {'admin': self}, name='mylinks_link_add_entry'),
        ]
        return urls + super().get_urls()


@admin.register(models.Embed)
class EmbedAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'url', 'site']
    raw_id_fields = ['site', ]
    exclude = ['created_at', 'subclass_type']
    search_fields = ['title', 'url', ]
    readonly_fields = ['markdown', 'html', 'data', 'source']
    inlines = [
        inlines.LinkTagItemInline,
    ]
