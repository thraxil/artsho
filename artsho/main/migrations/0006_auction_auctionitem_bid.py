# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_auto_20141028_2212'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateField(blank=True)),
                ('end', models.DateField(blank=True)),
                ('status', models.CharField(default=b'upcoming', max_length=32, choices=[(b'upcoming', b'upcoming'), (b'ongoing', b'ongoing'), (b'completed', b'completed')])),
                ('show', models.ForeignKey(to='main.Show')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuctionItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('starting_bid', models.PositiveIntegerField(default=1)),
                ('auction', models.ForeignKey(to='main.Auction')),
                ('item', models.ForeignKey(to='main.Item')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.PositiveIntegerField(default=1)),
                ('entered', models.DateTimeField(auto_now_add=True)),
                ('auctionitem', models.ForeignKey(to='main.AuctionItem')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
