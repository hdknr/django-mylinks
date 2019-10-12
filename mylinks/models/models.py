from django.db import models
from django.utils.translation import ugettext_lazy as _
from mytaggit.models import TaggableManager
from mylinks.oembed import get_oembed
from . import defs, methods, querysets


class Site(defs.Site):

    class Meta:
        verbose_name = _(' Site')
        verbose_name_plural = _(' Site')

    objects = querysets.SiteQuerySet.as_manager()

    def __str__(self):
        return self.name or ''


class Link(defs.Link):
    site = models.ForeignKey(
        Site, null=True, blank=True, default=None, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Web Link')
        verbose_name_plural = _('Web Link')

    tags = TaggableManager(blank=True)
    objects = querysets.LinkQuerySet.as_manager()

    def __str__(self):
        return self.title or self.url or ''

    def save(self, *args, **kwargs):
        self.update_site()
        super().save(*args, **kwargs)


class Embed(Link, defs.Embed):

    class Meta:
        verbose_name = _('Web Embed')
        verbose_name_plural = _('Web Embed')

    objects = querysets.EmbedQuerySet.as_manager()


def create_entry(url):
    oembed = get_oembed(url)
    if oembed.html:
        oembed.url = url
        return Embed.objects.create(**oembed.to_dict())
    else:
        return Link.objects.create(url=url, title=oembed.title)


class Feed(defs.Feed):

    class Meta:
        verbose_name = _('Feed')
        verbose_name_plural = _('Feeds')

    def __str__(self):
        return self.title or str(self.id)

class FeedEntry(defs.FeedEntry):
    link = models.ForeignKey(
        Link, null=True, blank=True, default=None, on_delete=models.SET_NULL)

    feeds = models.ManyToManyField(Feed, blank=True)
    class Meta:
        ordering = ['-published_at']
        verbose_name = _('Feed Entry')
        verbose_name_plural = _('Feed Entries')

    def __str__(self):
        return self.link and str(self.link) or str(self.id)

    objects = querysets.FeedEntryQuerySet.as_manager()
