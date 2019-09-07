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


def parse_text(html, selector):
    soup = Soup(html, 'html.parser')
    elms = soup and soup.select(selector)
    return elms and elms[0].text or ''

def parse_embed_url(html):
    '''parse oembed url from page'''
    soup = Soup(html, 'html.parser')
    items = soup and soup.select('link[type="application/json+oembed"]')
    return items and items[0].attrs['href']


def oembed_html(json_data):
    for i in ['html', 'rendered_body']:
        if i in json_data:
            return json_data[i]

def oembed_title(json_data):
    return json_data.get('title', None)

def api(url):
    res =  requests.get(url)
    if res.headers.get('Content-Type', '').startswith('application/json'):
        embed = oembed_html(res.json())
        title = oembed_title(res.json())
    else:
        embed = None
    return embed, title, res.text

def find(given_url):
    url, title, source, embed, data = None, None, None, None, None
    res = requests.get(given_url)

    if res and res.status_code == 200 \
            and res.headers.get('Content-Type', '').startswith('text/html'):
        url, source = parse_embed_url(res.text), res.text

    if url:
        embed, title, data = api(url)

    title = title or parse_text(source, 'title')

    return (url, title, embed, source, data)


def resolve(url):
    for pattern in PATTERN:
        match = re.search(pattern[0], url)
        if match:
            url = pattern[1].format(url=urlquote(url), **match.groupdict())
            embed, title, data = api(url)
            return (url, title, embed, None, data)

    return find(url)


def get_oembed(url, force_source=False):
    res = dict(zip(('url', 'title', 'html', 'source', 'data'), resolve(url)))    #(url, html
    return res
