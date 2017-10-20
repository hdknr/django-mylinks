# coding: utf-8
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import Client
from unittest import TestCase as UnitTestCase
from bs4 import BeautifulSoup as Soup
from urllib.parse import urlparse
from tests import models
import json


def contenttype(model):
    for_concrete_model = not model._meta.proxy
    return ContentType.objects.get_for_model(
        model, for_concrete_model=for_concrete_model)


class SimpleCase(UnitTestCase):

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
