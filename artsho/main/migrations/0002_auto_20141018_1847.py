# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


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
                ('image', models.TextField(default='', blank=True)),
                ('show', models.ForeignKey(to='main.Show', on_delete=models.CASCADE)),
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
