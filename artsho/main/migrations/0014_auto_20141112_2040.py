# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20141112_2002'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemPicture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.TextField(default='', blank=True)),
                ('item', models.ForeignKey(to='main.Item', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterOrderWithRespectTo(
            name='itempicture',
            order_with_respect_to='item',
        ),
    ]
