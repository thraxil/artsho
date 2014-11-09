# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bidauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='redirect_to',
            field=models.TextField(default='', blank=True),
            preserve_default=True,
        ),
    ]
