from django.utils.http import urlquote
from django.core.cache import cache
from django.utils.functional import cached_property

from bs4 import BeautifulSoup as Soup
from urllib.parse import urljoin

from dataclasses import field
import marshmallow
from marshmallow_dataclass import dataclass
from typing import ClassVar, Type
import requests
import re

TWITTER = "https://publish.twitter.com/oembed?url={url}"
INSTAGRAM = "https://api.instagram.com/oembed/?url={url}"
YOUTUBE = "http://www.youtube.com/oembed?url={url}&format=json"
QIITA = "http://qiita.com/api/v2/items/{id}"


PATTERN = [
    (r'(?P<scheme>https)\://(?P<host>www.youtube.com)(?P<path>/watch.+)', YOUTUBE),   # NOQA
    (r'(?P<scheme>https)\://(?P<host>www.instagram.com)(?P<path>/p/.+/)$', INSTAGRAM),  # NOQA
    (r'(?P<scheme>https)\://(?P<host>twitter.com)(?P<path>.+)$', TWITTER),
    (r'(?P<scheme>https*)\://(?P<host>qiita.com)(?P<path>.+/items/)(?P<id>.+)$', QIITA),   # NOQA
]


def get_soup(src, from_encoding=None, parser='html.parser'):
    return Soup(src, parser, from_encoding=from_encoding)


def parse_text(html, selector, from_encoding=None):
    soup = get_soup(html, from_encoding=from_encoding)
    elms = soup and soup.select(selector)
    return elms and elms[0].text or ''


def parse_embed_url(html, from_encoding=None):
    '''parse oembed url from page'''
    soup = get_soup(html, from_encoding=from_encoding)
    items = soup and soup.select('link[type="application/json+oembed"]')
    return items and items[0].attrs['href']


def oembed_html(json_data):
    for i in ['html', 'rendered_body']:
        if i in json_data:
            return json_data[i]


def oembed_title(json_data):
    return json_data.get('title', None)


def urlget(url, headers={}):
    UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    default_headers = {
        "User-Agent": UA,
        }
    default_headers.update(headers)

    res = requests.get(url, headers=default_headers)
    res.encoding = res.encoding if res.encoding in ['utf-8'] else res.apparent_encoding
    setattr(res, 'from_encoding', None if res.encoding in ['ISO-8859-1', 'ascii'] else res.encoding)
    return res

class Helper:
    @cached_property
    def schema(self):
        return self.__class__.Schema()

    def to_json(self, *args, **kwargs):
        return self.schema.dumps(self, *args, **kwargs)

    def to_dict(self, *args, **kwargs):
        return self.schema.dump(self, *args, **kwargs)

@dataclass
class Oembed(Helper):
    url:  str = field(
        default=None,
        metadata = { 
            "marshmallow_field": marshmallow.fields.Url()   # Custom marshmallow field
        })
    title: str = None
    html: str = None
    source: str = None
    data: str = None

    Schema: ClassVar[Type[marshmallow.Schema]] = marshmallow.Schema # For the type checker

    @classmethod
    def api(cls, url, source=None, from_encoding=None):
        res =  urlget(url)

        if res and res.headers.get('Content-Type', '').startswith('application/json'):
            html = oembed_html(res.json())
            title = oembed_title(res.json())
        else:
            html = None
            title = ''

        title = title or parse_text(source, 'title', from_encoding=from_encoding)
        return cls(url=url, html=html, title=title, data=res.text, source=source)

    @classmethod
    def find(cls, given_url):
        res = urlget(given_url)

        if res and res.status_code == 200 \
                and res.headers.get('Content-Type', '').startswith('text/html'):

            url, source = (
                parse_embed_url(res.text, from_encoding=res.from_encoding),
                res.text)

            if url:
                url = urljoin(given_url, url)   # url without hostname
                return cls.api(url, source=source, from_encoding=res.from_encoding)

            return cls(
                url=given_url, source=res.text,
                title=parse_text(res.text, 'title', from_encoding=res.from_encoding))

    @classmethod
    def create(cls, given_url):
        for pattern in PATTERN:
            match = re.search(pattern[0], given_url)
            if match:
                url = pattern[1].format(url=urlquote(given_url), **match.groupdict())
                return cls.api(url)

        return cls.find(given_url)


def get_oembed(url, force_source=False):
    return Oembed.create(url)
