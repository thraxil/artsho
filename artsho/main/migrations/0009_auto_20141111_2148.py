# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_bid_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='auctionitem',
        ),
        migrations.AlterField(
            model_name='bid',
            name='item',
            field=models.ForeignKey(to='main.Item', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
