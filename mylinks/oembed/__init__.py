# coding: utf-8
from django.utils.http import urlquote
from django.core.cache import cache
from bs4 import BeautifulSoup as Soup
from urllib.parse import urljoin
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

def api(url):
    res =  urlget(url)
    if res.headers.get('Content-Type', '').startswith('application/json'):
        embed = oembed_html(res.json())
        title = oembed_title(res.json())
    else:
        embed = None
        title = ''
    return embed, title, res.text

def urlget(url, headers={}):
    UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    default_headers = {
        "User-Agent": UA,
        }
    default_headers.update(headers)

    return requests.get(url, headers=default_headers)

def find(given_url):
    url, title, source, embed, data = None, None, None, None, None
    res = urlget(given_url)

    res.encoding = res.encoding if res.encoding in ['utf-8'] else res.apparent_encoding
    from_encoding = None if res.encoding in ['ISO-8859-1', 'ascii'] else res.encoding

    if res and res.status_code == 200 \
            and res.headers.get('Content-Type', '').startswith('text/html'):
        url, source = (
            parse_embed_url(res.text, from_encoding=from_encoding),
            res.text)
    else:
        # TODO: ERROR
        pass


    if url:
        url = urljoin(given_url, url) 
        embed, title, data = api(url)

    title = title or parse_text(source, 'title', from_encoding=from_encoding)

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
