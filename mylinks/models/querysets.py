from django.db import models

class SiteQuerySet(models.QuerySet):

    def create(self, host=None, name=None, *args, **kwargs):
        return host and self.filter(host=host).first() or\
            super().create(host=host, name=name, *args, **kwargs)


class LinkQuerySet(models.QuerySet):
    def create(self, url=None, **params):
        if self.filter(url=url).update(**params) > 0:
            return self.filter(url=url).first()
        return super().create(url=url, **params)


class EmbedQuerySet(models.QuerySet):

    @property
    def link_model(self):
        return self.model._meta.get_field('link_ptr').related_model

    def find_link(self, url):
        return self.link_model.objects.filter(url=url).first()

    def from_link(self, link, **params):
        params['url'] = params.get('url', link.url)
        params['title'] = params.get('title', link.title)
        # https://github.com/django/django/blob/master/django/db/models/base.py#L746
        self.model(link_ptr=link, **params).save_base(raw=True)
        return self.get(id=link.id)

    def create(self, url=None, **params):
        if self.filter(url=url).update(**params) > 0:
            return self.filter(url=url).first()

        link = self.find_link(url)
        if link:
            return self.from_link(link, **params)

        return super().create(url=url, **params)
