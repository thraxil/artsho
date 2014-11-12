# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_item_auction'),
    ]

    operations = [
        migrations.AlterOrderWithRespectTo(
            name='item',
            order_with_respect_to='auction',
        ),
        migrations.RemoveField(
            model_name='item',
            name='show',
        ),
    ]
