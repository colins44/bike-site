# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0005_auto_20151008_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bikesearch',
            name='bike_type',
            field=models.CharField(max_length=225, choices=[(b'road_bike', b'road bike'), (b'mountain_bike', b'mountain bike'), (b'touring_bicycle', b'touring bicycle'), (b'electric_bicycle', b'electric bicycle'), (b'cruiser_bike', b'cruiser bicycle'), (b'scooter', b'scooter')]),
        ),
    ]
