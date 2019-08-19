from django.db import models
from django.utils.translation import ugettext_lazy as _
from . import defs, methods, querysets


class Site(defs.Site, methods.Site):

    class Meta:
        verbose_name = _(' Site')
        verbose_name_plural = _(' Site')

    def __str__(self):
        return self.name or ''


class Link(defs.Link, methods.Link):
    site = models.ForeignKey(
        Site, null=True, blank=True, default=None, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Web Link')
        verbose_name_plural = _('Web Link')

    objects = querysets.LinkQuerySet.as_manager()

    def __str__(self):
        return self.title or self.url
        
    def save(self, *args, **kwargs):
        self.update_site()
        super(Link, self).save(*args, **kwargs)


class Page(defs.Page, methods.Page):
    site = models.ForeignKey(
        Site, null=True, blank=True, default=None, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Web Page')
        verbose_name_plural = _('Web Page')

    objects = querysets.PageQuerySet.as_manager()

    def __str__(self):
        return self.title or self.url

    def save(self, *args, **kwargs):
        self.update_site()
        self.update_content()
        super(Page, self).save(*args, **kwargs)
