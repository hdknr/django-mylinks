from django.utils.html import mark_safe
from django.utils.functional import cached_property

from bs4 import BeautifulSoup as Soup
from urllib.parse import urlparse
from mylinks.oembed import get_oembed
import re


def is_ascii(s):
    return bool(re.match(r'[\x00-\x7F]+$', s))


class Site(object):

    @property
    def url(self):
        return u"http://{}/".format(self.host)


class Link(object):

    def update_site(self):
        SiteModel = self._meta.get_field('site').related_model
        url = self.url and urlparse(self.url)
        if not url or not url.netloc:
            return
            
        if not self.site or self.site.host != url.netloc:
            self.site = SiteModel.objects.create(
                host=url.netloc, name=url.netloc)

    @classmethod
    def create_link(cls, url, with_content=True):
        link, created = cls.objects.get_or_create(url=url)
        if with_content:
            link.add_content()
        return link


    @classmethod
    def content_manager(cls):
        return cls._meta.get_field('content').related_model.objects
        
    def add_content(self):
        e = get_oembed(self.url)

        if e['url']:
            man = self.content_manager()
            qs = man.filter(url=e['url'])
            if qs.update(embed=e['html'], source=e['source'], data=e['data']) > 0:
                self.content = qs.first()
            else:
                self.content = man.create(
                    url=e['url'], embed=e['html'], source=e['source'], data=e['data'])
        else: 
            title = Soup(embed['source'], 'html.parser').select('title')
            self.title = title and title[0] or self.title

        self.save()

    @property
    def embed_html(self):
        return self.content and self.content.embed and self.content.embed_html


class Content(Link):

    def get_html(self):
        return get_html(self.url)

    def update_content(self):
        oembed = self.get_html()
        self.source = oembed['source']  # .encode('utf8')
        self.embed= oembed['html']

    @cached_property
    def embed_soup(self):
        return self.embed and Soup(self.embed, 'html.parser')

    @property
    def embed_html(self):
        return self.embed and mark_safe(self.embed)

