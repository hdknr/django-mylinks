from bs4 import BeautifulSoup as Soup
from urllib.parse import urlparse
from mylinks.oembed import get_html


class Site(object):

    @property
    def url(self):
        return u"http://{}/".format(self.host)


class Page(object):

    def update_site(self):
        from . import models
        url = self.url and urlparse(self.url)
        if not self.site or self.site.host != url.netloc:
            self.site = models.Site.objects.filter(
                host=url.netloc).first() or models.Site.objects.create(
                    host=url.netloc, name=url.netloc)

    def get_html(self):
        return get_html(self.url)

    def update_content(self):
        oembed = self.get_html()
        self.source = oembed['source']  # .encode('utf8')
        self.embed = oembed['html']
        self.title = self.title or self.source_title
        self.save()

    @property
    def source_soup(self):
        if not hasattr(self, '_soup'):
            self._soup = self.source and Soup(self.source, 'html.parser')
        return self._soup

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
