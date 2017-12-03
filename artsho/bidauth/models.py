from django.db import models
from django.contrib.auth.models import User
from itsdangerous import URLSafeSerializer
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
import time


class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField(blank=False, db_index=True)
    redirect_to = models.TextField(blank=True, default=u"")


def make_token(user, redirect="/"):
    s = URLSafeSerializer(settings.BIDAUTH_SECRET)
    return Token.objects.create(
        user=user,
        token=s.dumps(dict(
            email=user.email,
            timestamp=time.time()
        )),
        redirect_to=redirect,
    )


def make_and_email_token(user, redirect="/"):
    # first, we take a moment to clean out old tokens for this user
    Token.objects.filter(user=user).delete()
    t = make_token(user, redirect)
    send_mail(
        "Artsho login",
        (
            """To login, just visit this page:\n\n"""
            """%s%s?token=%s"""
            """\n\nThis link will be valid for one hour.\n"""
        ) % (
            settings.SITE_BASE,
            reverse('bidauth_login'),
            t.token),
        settings.SERVER_EMAIL,
        [user.email],
        fail_silently=settings.DEBUG
    )
