# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0024_auto_20160113_1933'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('bike_shop', models.OneToOneField(to='bike_aggregator.BikeShop')),
                ('rental_equipment', models.OneToOneField(to='bike_aggregator.RentalEquipment')),
            ],
        ),
    ]
