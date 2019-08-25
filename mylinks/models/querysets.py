from django.db import models

class SiteQuerySet(models.QuerySet):

    def create(self, host=None, name=None, *args, **kwargs):
        return host and self.filter(host=host).first() or\
            super().create(host=host, name=name, *args, **kwargs)


class LinkQuerySet(models.QuerySet):
    def create(self, url=None, *args, **kwargs):
        return self.filter(url=url).first() or\
            super().create(url=url, *args, **kwargs)


class PageQuerySet(LinkQuerySet):
    pass
