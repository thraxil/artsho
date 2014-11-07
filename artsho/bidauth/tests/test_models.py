from artsho.bidauth.models import Token, make_and_email_token
from django.test import TestCase
from django.contrib.auth.models import User


class TestToken(TestCase):
    pass


class TestMakeAndEmail(TestCase):
    def test_simple(self):
        u = User.objects.create(username='foo')
        make_and_email_token(u)
        self.assertEqual(Token.objects.filter(user=u).count(), 1)
