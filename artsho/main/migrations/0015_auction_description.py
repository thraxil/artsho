# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20141112_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='description',
            field=models.TextField(default='', blank=True),
            preserve_default=True,
        ),
    ]
