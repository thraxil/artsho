# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20141111_2148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionitem',
            name='starting_bid',
        ),
        migrations.AddField(
            model_name='item',
            name='starting_bid',
            field=models.PositiveIntegerField(default=1),
            preserve_default=True,
        ),
    ]
