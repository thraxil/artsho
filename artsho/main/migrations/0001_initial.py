# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(default='ARTSHO', blank=True)),
                ('year', models.IntegerField(default=2014)),
                ('location', models.TextField(default='', blank=True)),
                ('description', models.TextField(default='', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
