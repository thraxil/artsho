from django.test import TestCase
from django.test.client import Client
from .factories import (
    NewsItemFactory, ShowFactory,
    PictureFactory, ShowVideoFactory,
)
from django.contrib.auth.models import User


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


class EditTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.u = User.objects.create(username='test')
        self.u.set_password('test')
        self.u.save()
        self.c.login(username='test', password='test')

    def test_edit_index(self):
        r = self.c.get("/edit/")
        self.assertEqual(r.status_code, 200)

    def test_edit_show_form(self):
        s = ShowFactory()
        r = self.c.get("/edit/show/%d/" % s.id)
        self.assertEqual(r.status_code, 200)

    def test_edit_show(self):
        s = ShowFactory()
        r = self.c.post(
            "/edit/show/%d/" % s.id,
            dict(title="new title", year="1999")
        )
        self.assertEqual(r.status_code, 302)
        r = self.c.get("/edit/show/%d/" % s.id)
        self.assertEqual(r.status_code, 200)
        self.assertTrue("new title" in r.content)

    def test_add_video(self):
        s = ShowFactory()
        r = self.c.post(
            "/edit/show/%d/add_video/" % s.id,
            dict(youtube_id="foobar")
        )
        self.assertEqual(r.status_code, 302)
        r = self.c.get("/edit/show/%d/" % s.id)
        self.assertEqual(r.status_code, 200)
        self.assertTrue("iframe" in r.content)

    def test_delete_picture(self):
        p = PictureFactory()
        r = self.c.post(
            "/edit/picture/%d/delete/" % p.id,
            dict()
        )
        self.assertEqual(r.status_code, 302)

    def test_delete_video(self):
        p = ShowVideoFactory()
        r = self.c.post(
            "/edit/showvideo/%d/delete/" % p.id,
            dict()
        )
        self.assertEqual(r.status_code, 302)

    def test_add_picture(self):
        s = ShowFactory()
        with open('media/img/artsho5_poster.png') as img:
            r = self.c.post(
                "/edit/show/%d/add_picture/" % s.id,
                dict(image=img))
            self.assertEqual(r.status_code, 302)

    def test_add_picture_unsupported_extension(self):
        s = ShowFactory()
        with open('media/robots.txt') as img:
            r = self.c.post(
                "/edit/show/%d/add_picture/" % s.id,
                dict(image=img))
            self.assertEqual(r.status_code, 302)
