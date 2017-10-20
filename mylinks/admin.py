from django.contrib import admin
from . import models


class LinkAdminInline(admin.TabularInline):
    model = models.Link
    extra = 1


@admin.register(models.Word)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', ]
    inlines = [LinkAdminInline]
