from django.db import models
from django.utils.translation import ugettext_lazy as _
from . import methods


class Site(models.Model, methods.Site):
    host = models.CharField(
        _('Site Host Name'), max_length=50, unique=True, db_index=True)

    name = models.CharField(
        _('Site Name'), max_length=100)

    brand = models.TextField(
        _('Site Brand'),
        null=True, default=None, blank=True)

    class Meta:
        abstract = True


class Link(models.Model, methods.Link):

    url = models.CharField(
        _('Link URL'), unique=True, db_index=True,
        max_length=200, validators=[methods.is_ascii])

    title = models.CharField(
        _('Title'), max_length=250,
        null=True, blank=True, default=None)

    class Meta:
        abstract = True


class Page(models.Model, methods.Page):

    url = models.URLField(
        _('Link URL'), unique=True, db_index=True)

    embed = models.TextField(
        _('Embed HTML'),
        null=True, default=None, blank=True)

    title = models.CharField(
        _('Title'), max_length=250,
        null=True, blank=True, default=None)

    source = models.TextField(
        _('Source HTML'),
        null=True, default=None, blank=True)

    class Meta:
        abstract = True
