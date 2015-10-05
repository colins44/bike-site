# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BikeSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.CharField(max_length=225)),
                ('bike_type', models.CharField(max_length=225, choices=[(b'road_bike', b'road bike'), (b'mountain_bike', b'mountain bike'), (b'hybrid_bike', b'hybrid bike'), (b'touring_bike', b'touring bike'), (b'electric_bike', b'electric bike')])),
                ('no_of_bikes', models.IntegerField()),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
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
