from django.db import models


class LinkQuerySet(models.QuerySet):
    def create(self, url=None, *args, **kwargs):
        return self.filter(url=url).first() \
            or super(LinkQuerySet, self).create(url=url, *args, **kwargs)


class PageQuerySet(LinkQuerySet):
    pass
