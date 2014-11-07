from django.db import models
from django.contrib.auth.models import User
from itsdangerous import URLSafeSerializer
from django.conf import settings
import time


class Token(models.Model):
    user = models.ForeignKey(User)
    token = models.TextField(blank=False, db_index=True)


def make_token(user):
    s = URLSafeSerializer(settings.BIDAUTH_SECRET)
    return Token.objects.create(
        user=user,
        token=s.dumps(dict(
            email=user.email,
            timestamp=time.time()
        ))
    )


def make_and_email_token(user):
    # first, we take a moment to clean out old tokens for this user
    Token.objects.filter(user=user).delete()
    t = make_token(user)
    print "http://localhost:8000/bidauth/login/?token=" + t.token
