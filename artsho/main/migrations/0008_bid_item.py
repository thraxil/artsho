# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20141106_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='item',
            field=models.ForeignKey(to='main.Item', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
