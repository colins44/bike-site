# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BikeSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('town_or_region', models.CharField(max_length=225)),
                ('country', models.CharField(max_length=225)),
                ('bike_type', models.CharField(max_length=225, choices=[(b'road_bike', b'road bike'), (b'mountain_bike', b'mountain bike'), (b'hybrid_bike', b'hybrid bike'), (b'touring_bike', b'touring bike'), (b'electric_bike', b'electric bike')])),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='BikeShop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('town_or_region', models.CharField(max_length=225)),
                ('country', models.CharField(max_length=225)),
                ('shop_name', models.CharField(max_length=225)),
                ('website', models.URLField(null=True, blank=True)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
