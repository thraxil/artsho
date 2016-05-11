from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def reticulum_url(rkey, basename, ext, size):
    return "{}/image/{}/{}/{}{}".format(
        settings.RETICULUM_PUBLIC_BASE, rkey, size,
        basename, ext)
