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
    '''parse oembed url from page'''
    soup = Soup(html, 'html.parser')
    items = soup and soup.select('link[type="application/json+oembed"]')
    return items and items[0].attrs['href']


def oembed_html(json_data):
    for i in ['html', 'rendered_body']:
        if i in json_data:
            return json_data[i]


def find(given_url):
    url, source, embed, data = None, None, None, None
    res = requests.get(given_url)
    if res and res.status_code == 200 \
            and res.headers.get('Content-Type', '').startswith('text/html'):
        url, source = parse_embed_url(res.text), res.text

    if url:
        res =  requests.get(url)
        embed = oembed_html(res.json())
        data = res.text

    return (url, embed, source, data)


def resolve(url):
    for pattern in PATTERN:
        match = re.search(pattern[0], url)
        if match:
            url = pattern[1].format(url=urlquote(url), **match.groupdict())
            res = requests.get(url)
            return (url, oembed_html(res.json()), None, res.text)

    return find(url)


def get_oembed(url, force_source=False):
    return dict(zip(('url', 'html', 'source', 'data'), resolve(url)))    #(url, html
