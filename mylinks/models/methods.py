from django.utils.html import mark_safe
from django.utils.functional import cached_property
from django.utils import timezone

from bs4 import BeautifulSoup as Soup
from urllib.parse import urlparse
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
