from django.core.management.base import BaseCommand
from artsho.main.models import Show, Picture
import os
from datetime import datetime
from django.conf import settings
import shutil


class Command(BaseCommand):
    def handle(self, show_id, *args, **kwargs):
        s = Show.objects.get(id=show_id)
        now = datetime.now()
        for f in args:
            basename = os.path.basename(f).lower()
            print basename
            path = "pictures/%04d/%02d/%02d/" % (
                now.year, now.month, now.day)
            try:
                os.path.makedirs(
                    os.path.join(settings.MEDIA_ROOT, path)
                )
            except:
                pass
            shutil.copyfile(
                f, os.path.join(settings.MEDIA_ROOT, path, basename))
            Picture.objects.create(
                show=s,
                title=basename,
                image="pictures/%04d/%02d/%02d/%s" % (
                    now.year, now.month, now.day,
                    basename
                )
            )
