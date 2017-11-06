# coding: utf-8
from django.utils.http import urlquote
from django.core.cache import cache
from bs4 import BeautifulSoup as Soup
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


def parse_embed_url(html):
    soup = Soup(html, 'html.parser')
    items = soup and soup.select('link[type="application/json+oembed"]')
    return items and items[0].attrs['href']


def find(url):
    res = requests.get(url)
    if res and res.status_code == 200 \
            and res.headers.get('Content-Type', '').startswith('text/html'):
        return (parse_embed_url(res.text), res.text)
    return (None, res.text)


def get(url):
    for pattern in PATTERN:
        match = re.search(pattern[0], url)
        if match:
            url = pattern[1].format(url=urlquote(url), **match.groupdict())
            return (url, requests.get(url).text)
    return find(url)


def get_html(url, force_source=False):
    items = ['url', 'source', 'html', ]
    oembed = dict((k, cache.get("oembed:{}:{}".format(k, url))) for k in items)

    if not oembed['html']:
        oembed['url'], oembed['source'] = get(url)
        if oembed['url']:
            res = requests.get(oembed['url']).json()
            for i in ['html', 'rendered_body']:
                if i in res:
                    oembed['html'] = res[i]
                    break

        map(lambda k: cache.set("oembed:{}:{}".format(k, url), oembed[k]),
            items)

    return oembed
