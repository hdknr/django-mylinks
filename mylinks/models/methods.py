from django.utils.html import mark_safe
from django.utils.functional import cached_property
from django.utils import timezone

from bs4 import BeautifulSoup as Soup
from urllib.parse import urlparse
from mylinks.oembed import get_oembed
import json
import re


def is_ascii(s):
    return bool(re.match(r'[\x00-\x7F]+$', s))


class Site(object):

    @property
    def url(self):
        return u"http://{}/".format(self.host)


class Link(object):

    @property
    def markdown(self):
        title = self.title.replace('|', '-')   # STOP Jekyll making tables
        return f"[{title}]({self.url})"

    @classmethod
    def get_soup(cls, text, parser='html.parser'):
        return Soup(text, parser)

    def update_site(self):
        SiteModel = self._meta.get_field('site').related_model
        url = self.url and urlparse(self.url)
        if not url or not url.netloc:
            return
            
        if not self.site or self.site.host != url.netloc:
            self.site = SiteModel.objects.create(
                host=url.netloc, name=url.netloc)
    @property
    def embed_html(self):
        return hasattr(self, 'embed') and self.embed.safe_html or ''

class Hoge:

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

        if e['url'] and e['html']:
            man = self.content_manager()
            qs = man.filter(url=e['url'])
            if qs.update(embed=e['html'], source=e['source'], data=e['data']) > 0:
                self.content = qs.first()
            else:
                self.content = man.create(
                    url=e['url'], embed=e['html'], source=e['source'], data=e['data'],
                )
            self.title = self.content.data_dict.get('title', self.title) 
        else: 
            title = Soup(e['source'], 'html.parser').select('title')
            self.title = title and title[0].text or self.title

        self.save()


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

    @property
    def data_dict(self):
        return self.data and json.loads(self.data) or {}


class Embed(object):

    def get_html(self):
        return get_html(self.url)

    def update_content(self):
        oembed = self.get_html()
        self.source = oembed['source']  # .encode('utf8')
        self.html = oembed['html']

    @cached_property
    def html_soup(self):
        return self.html and Soup(self.html, 'html.parser')

    @property
    def safe_html(self):
        return self.html and mark_safe(self.html)

    @property
    def data_dict(self):
        return self.data and json.loads(self.data) or {}
