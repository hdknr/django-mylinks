from django.db import models


class PageQuerySet(models.QuerySet):

    def create(self, url=None, *args, **kwargs):
        return self.filter(url=url).first() \
            or super(PageQuerySet, self).create(url=url, *args, **kwargs)
