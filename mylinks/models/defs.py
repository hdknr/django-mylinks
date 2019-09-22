from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from . import methods


class SuperModel(models.Model):
    subclass_type = models.ForeignKey(
        ContentType, verbose_name=_("Subclass Type"), 
        limit_choices_to={'app_label': 'mylinks'},
        null=True, blank=True, default=None,
        on_delete=models.SET_NULL)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self._meta.parents:
            self.subclass_type = kwargs.get(
                'subclass_type', ContentType.objects.get_for_model(self))
        super(SuperModel, self).save(*args, **kwargs)

    @property
    def instance(self):
        return self.subclass_type and \
            self.subclass_type.get_object_for_this_type(id=self.id) or self

    @classmethod
    def superclass(cls):
        return cls._meta.parents and next(iter(cls._meta.parents)) or None 

    @classmethod
    def superclass_type(cls):
        return cls.superclass() and ContentType.objects.get_for_model(cls.superclass())

    @property
    def model(self):
        return self.subclass_type and self.subclass_type.model

    def delete_self(self, *args, **kwargs):
        '''delete on only subclass instance and `keep parents` '''
        superclass= self.superclass()
        if superclass:
            superclass_type = superclass._meta.parents and self.superclass_type() or None
            superclass.objects.filter(id=self.id).update(subclass_type=superclass_type)
        # https://docs.djangoproject.com/en/1.10/ref/models/instances/#django.db.models.Model.delete
        kwargs['keep_parents'] = True
        super().delete(*args, **kwargs)


class Timestamp(models.Model):
    created_at = models.DateTimeField(_('Created At'), default=timezone.now) 
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        abstract = True


class Site(Timestamp, methods.Site):
    host = models.CharField(
        _('Site Host Name'), max_length=50, unique=True, db_index=True)

    name = models.CharField(
        _('Site Name'), max_length=100)

    brand = models.TextField(
        _('Site Brand'),
        null=True, default=None, blank=True)

    class Meta:
        abstract = True


class Entry(models.Model):

    url = models.CharField(
        _('Link URL'), unique=True, db_index=True,
        max_length=400, validators=[methods.is_ascii])

    class Meta:
        abstract = True


class Link(SuperModel, Entry, Timestamp, methods.Link):

    title = models.CharField(
        _('Title'), max_length=250,
        null=True, blank=True, default=None)

    visited_at = models.DateTimeField(
        null=True, default=timezone.now, blank=True)
    enabled = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Embed(models.Model, methods.Embed):
    url = models.CharField(
        _('Embed URL'), unique=True, db_index=True,
        max_length=400, validators=[methods.is_ascii])

    html = models.TextField(
        _('Embed HTML'),
        null=True, default=None, blank=True)

    data = models.TextField(
        _('Embed JSON'),
        null=True, default=None, blank=True)

    source = models.TextField(
        _('Page Source HTML'),
        null=True, default=None, blank=True)


    class Meta:
        abstract = True
