# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from . import defs, methods


class Site(defs.Site, methods.Site):

    class Meta:
        verbose_name = _(' Site')
        verbose_name_plural = _(' Site')

    def __unicode__(self):
        return self.name or ''


class Page(defs.Page, methods.Page):

    site = models.ForeignKey(Site, null=True, blank=True, default=None)

    class Meta:
        verbose_name = _('Web Page')
        verbose_name_plural = _('Web Page')

    def __unicode__(self):
        return self.title or self.url

    def save(self, *args, **kwargs):
        self.update_site()
        super(Page, self).save(*args, **kwargs)
