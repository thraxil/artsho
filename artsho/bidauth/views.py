from django.contrib.auth.models import User
from django.views.generic import View
from django.http import (
    HttpResponseRedirect, HttpResponse)
from django.shortcuts import render
import uuid
from itsdangerous import URLSafeSerializer
import time
from .models import make_and_email_token, Token
from django.contrib.auth import login as django_login
from django.conf import settings


def within_an_hour(timestamp):
    now = time.time()
    return abs(now - timestamp) < 3600


def make_new_user(email):
    u = User.objects.create(
        username=str(uuid.uuid4())[:25],
        first_name=str(uuid.uuid4())[:25],
        last_name=str(uuid.uuid4())[:25],
        email=email.lower(),
        is_staff=False,
        is_superuser=False)
    u.set_unusable_password()
    u.save()
    return u


def get_or_create_user(email):
    r = User.objects.filter(email=email.lower())
    if r.count() == 0:
        return make_new_user(email)
    return r[0]


class LoginView(View):
    template_name = "bidauth/login.html"

    def get(self, request):
        if not request.user.is_anonymous:
            return HttpResponse("you are already logged in...")

        token = request.GET.get('token', False)
        if token:
            return self.validate_token(request, token)
        return render(request, self.template_name, dict())

    def validate_token(self, request, token):
        s = URLSafeSerializer(settings.BIDAUTH_SECRET)
        sig_ok, payload = s.loads_unsafe(token)
        if not sig_ok:
            return HttpResponse("bad token")
        email = payload['email']
        if not within_an_hour(payload['timestamp']):
            # token's only valid for an hour
            return HttpResponse("stale token")
        r = Token.objects.filter(
            token=token,
            user__email=email)
        if r.count() == 0:
            return HttpResponse("token not found. probably already used")
        u = r[0].user
        u.backend = 'django.contrib.auth.backends.ModelBackend'
        django_login(request, u)
        redirect = r[0].redirect_to
        r[0].delete()
        return HttpResponseRedirect(redirect)

    def post(self, request):
        email = request.POST.get('email', '')
        if email == '':
            return HttpResponse("please enter an email address")

        u = get_or_create_user(email)
        make_and_email_token(
            u,
            redirect=request.POST.get('next', '/'))
        return HttpResponse("you have been emailed a login link")
