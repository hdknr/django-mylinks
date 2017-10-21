from django.contrib import admin
from . import models


class PageAdminInline(admin.TabularInline):
    model = models.Page
    extra = 1


@admin.register(models.Site)
class SiteAdmin(admin.ModelAdmin):
    inlines = [PageAdminInline]
