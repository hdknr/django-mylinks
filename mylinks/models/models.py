from django.db import models
from django.utils.translation import ugettext_lazy as _
from mytaggit.models import TaggableManager
from . import defs, methods, querysets


class Site(defs.Site):

    class Meta:
        verbose_name = _(' Site')
        verbose_name_plural = _(' Site')

    objects = querysets.SiteQuerySet.as_manager()

    def __str__(self):
        return self.name or ''


class Content(defs.Content):
    objects = querysets.ContentQuerySet.as_manager()

    class Meta:
        verbose_name = _('Web Conent')
        verbose_name_plural = _('Web Contents')


class Link(defs.Link):
    site = models.ForeignKey(
        Site, null=True, blank=True, default=None, on_delete=models.CASCADE)

    content = models.ForeignKey(
        Content, 
        null=True, default=None, blank=True,
        on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Web Link')
        verbose_name_plural = _('Web Link')

    tags = TaggableManager(blank=True)
    objects = querysets.LinkQuerySet.as_manager()

    def __str__(self):
        return self.title or self.url
        
    def save(self, *args, **kwargs):
        self.update_site()
        super().save(*args, **kwargs)
