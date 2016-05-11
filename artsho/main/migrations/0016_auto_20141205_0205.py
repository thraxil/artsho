# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auction_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='image',
            field=models.TextField(default='', blank=True),
            preserve_default=True,
        ),
    ]
