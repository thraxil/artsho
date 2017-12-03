# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20141111_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='auction',
            field=models.ForeignKey(default=0, to='main.Auction', on_delete=models.CASCADE),
            preserve_default=False,
        ),
    ]
