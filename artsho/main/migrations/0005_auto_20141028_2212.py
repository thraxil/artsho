# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20141027_2141'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShowVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('youtube_id', models.TextField()),
                ('show', models.ForeignKey(to='main.Show')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterOrderWithRespectTo(
            name='showvideo',
            order_with_respect_to='show',
        ),
    ]
