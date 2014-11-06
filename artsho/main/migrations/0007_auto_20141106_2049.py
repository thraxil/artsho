# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auction_auctionitem_bid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bid',
            options={'ordering': ('-amount',)},
        ),
        migrations.AlterOrderWithRespectTo(
            name='auctionitem',
            order_with_respect_to='auction',
        ),
    ]
