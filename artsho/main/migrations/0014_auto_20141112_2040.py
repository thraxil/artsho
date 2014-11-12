# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20141112_2002'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemPicture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', sorl.thumbnail.fields.ImageWithThumbnailsField(null=True, upload_to=b'itempictures/%Y/%m/%d')),
                ('item', models.ForeignKey(to='main.Item')),
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
