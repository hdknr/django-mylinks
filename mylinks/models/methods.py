from django.utils.html import mark_safe
from django.utils.functional import cached_property

from bs4 import BeautifulSoup as Soup
from urllib.parse import urlparse
from mylinks.oembed import get_html
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


class Page(Link):

    def get_html(self):
        return get_html(self.url)

    def update_content(self):
        oembed = self.get_html()
        self.source = oembed['source']  # .encode('utf8')
        self.embed = oembed['html']
        self.title = self.title or self.source_title

    @cached_property
    def source_soup(self):
        return self.source and Soup(self.source, 'html.parser')

    @cached_property
    def embed_soup(self):
        return self.embed and Soup(self.embed, 'html.parser')

    @property
    def source_title(self):
        title = self.source_soup and self.source_soup.select('title')
        title = title and title[0]
        return title and title.text or ''

    @property
    def source_images(self):

        def _U(u):
            if parse.urlparse(u).netloc:
                return u
            return parse.urljoin(self.url, u)

        if not self.source_soup:
            return []
        srcs = [_U(e.attrs['src'])
                for e in self.source_soup.select('img') if 'src' in e.attrs]

        return list(sorted(set(srcs)))

    @property
    def embed_html(self):
        return self.embed and mark_safe(self.embed)