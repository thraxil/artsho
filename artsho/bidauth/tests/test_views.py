from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from artsho.bidauth.models import make_token
from django.utils.encoding import force_text
from django.urls import reverse


class LoginGetTest(TestCase):
    def test_already_logged_in(self):
        u = User.objects.create(username='foo')
        u.set_password('test')
        u.save()
        c = Client()
        c.login(username='foo', password='test')
        r = c.get(reverse("bidauth_login"))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(force_text(r.content), "you are already logged in...")

    def test_not_logged_in_and_no_token(self):
        c = Client()
        r = c.get(reverse("bidauth_login"))
        self.assertEqual(r.status_code, 200)
        self.assertTrue("<form" in force_text(r.content))

    def test_invalid_token(self):
        c = Client()
        r = c.get(reverse("bidauth_login"), dict(token='not-valid'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(force_text(r.content), "bad token")

    def test_valid_but_stale_token(self):
        t = ('eyJ0aW1lc3RhbXAiOjAuMCwiZW1haWwiOiJzb21lb25lQGV4YW'
             '1wbGUuY29tIn0.p9nLB0aJNQD-aNq4OC_kquL-gic')
        c = Client()
        r = c.get(reverse("bidauth_login"), dict(token=t))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(force_text(r.content), "stale token")

    def test_good_token(self):
        u = User.objects.create(
            username='asdf',
            email='someone@example.com')
        t = make_token(u)
        c = Client()
        r = c.get(reverse("bidauth_login"), dict(token=t.token))
        self.assertEqual(r.status_code, 302)

    def test_good_but_missing_token(self):
        u = User.objects.create(
            username='asdf',
            email='someone@example.com')
        t = make_token(u)
        token = t.token
        t.delete()
        c = Client()
        r = c.get(reverse("bidauth_login"), dict(token=token))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(force_text(r.content),
                         "token not found. probably already used")


class LoginPostTest(TestCase):
    def test_no_email(self):
        c = Client()
        r = c.post(reverse('bidauth_login'),
                   dict(email=''))
        self.assertEqual(force_text(r.content),
                         "please enter an email address")

    def test_existing_user(self):
        User.objects.create(username='foo', email='existing@example.com')
        c = Client()
        r = c.post(reverse('bidauth_login'),
                   dict(email='existing@example.com'))
        self.assertEqual(force_text(r.content),
                         "you have been emailed a login link")

    def test_new_user(self):
        c = Client()
        r = c.post(reverse('bidauth_login'),
                   dict(email='newemail@example.com'))
        self.assertEqual(force_text(r.content),
                         "you have been emailed a login link")
