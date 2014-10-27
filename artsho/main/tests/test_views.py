from django.test import TestCase
from django.test.client import Client
from .factories import NewsItemFactory


class BasicTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_smoketest(self):
        response = self.c.get("/smoketest/")
        self.assertEquals(response.status_code, 200)


class IndexTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_empty(self):
        response = self.c.get("/")
        self.assertEquals(response.status_code, 200)

    def test_news_item(self):
        NewsItemFactory()
        response = self.c.get("/")
        self.assertEquals(response.status_code, 200)
        self.assertTrue("test news item" in response.content)
