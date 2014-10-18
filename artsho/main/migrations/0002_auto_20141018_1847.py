# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(default='', blank=True)),
                ('caption', models.TextField(default='', blank=True)),
                ('image', sorl.thumbnail.fields.ImageWithThumbnailsField(null=True, upload_to=b'pictures/%Y/%m/%d')),
                ('show', models.ForeignKey(to='main.Show')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterOrderWithRespectTo(
            name='picture',
            order_with_respect_to='show',
        ),
        migrations.AlterModelOptions(
            name='show',
            options={'ordering': ['year']},
        ),
    ]
