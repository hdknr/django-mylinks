# coding: utf-8
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import Client
from unittest import TestCase as UnitTestCase
from bs4 import BeautifulSoup as Soup
from urllib.parse import urlparse, parse_qs
from tests import models
from mylinks import oembed
from mylinks.models import Page
import json


def contenttype(model):
    for_concrete_model = not model._meta.proxy
    return ContentType.objects.get_for_model(
        model, for_concrete_model=for_concrete_model)


class PageCase(UnitTestCase):

    def test_twitter(self):
        url = 'https://twitter.com/MLIT_JAPAN/status/921293269291565058'
        page = Page(url=url)
        page.update_content()
        node = Soup(page.embed, "html5lib").select('a')[-1]
        self.assertTrue(node['href'].startswith(url))

    def test_facebook(self):
        url = 'https://www.facebook.com/marketingjapan/posts/1068775179876599'
        page = Page(url=url)
        page.update_content()
        # page.embed is javascript

    def test_wordpress(self):
        '''
            <link rel="alternate" type="text/xml+oembed"
                href="https://ja.wordpress.org/wp-json/oembed/1.0/embed?url=https%3A%2F%2Fja.wordpress.org%2F&amp;format=xml">
        '''
        url = 'https://ja.wordpress.org/'
        page = Page(url=url)
        page.update_content()
        node = Soup(page.embed, "html5lib").select('iframe')[-1]
        self.assertEqual(url + 'embed/', node['src'])

    def test_instagram(self):
        url = 'https://www.instagram.com/p/BagxHa_AupI/'
        page = Page(url=url)
        page.update_content()
        node = Soup(page.embed, "html5lib").select('a')[-1]
        self.assertEqual(url, node['href'])

    def test_youtube(self):
        url = 'https://www.youtube.com/watch?v=wF-4-DcCQoI'
        v = parse_qs(urlparse(url).query)['v'][0]
        page = Page(url=url)
        page.update_content()
        node = Soup(page.embed, "html5lib").select('iframe')[-1]
        src = 'https://www.youtube.com/embed/{}?feature=oembed'.format(v)
        self.assertEqual(src, node['src'])

    def test_qiita(self):
        url = 'https://qiita.com/nonbiri15/items/d36ba908c8469cc97518'
        page = Page(url=url)
        page.update_content()


class OembedCase(UnitTestCase):

    def setUp(self):
        self.instance = models.Article.objects.create(
            author='author', title='title')
        self.client = Client()

    def test_api(self):
        ct = contenttype(self.instance)
        key = ".".join(ct.natural_key())
        url = reverse(
            'mylinks_oembed_api',
            kwargs=dict(content_type=key, id=self.instance.id))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content.decode('utf-8'))
        node = Soup(data['html'], "html5lib").select('script')[0]
        path = urlparse(node['src']).path
        url = reverse(
            'mylinks_oembed_script',
            kwargs=dict(content_type=key, id=self.instance.id))
        self.assertEqual(path, url)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse(
            'mylinks_oembed_widget',
            kwargs=dict(content_type=key, id=self.instance.id))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        node = Soup(response.content, "html5lib").select('a')[0]
