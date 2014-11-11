# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20141111_2154'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AuctionItem',
        ),
    ]
