# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0026_prices_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prices',
            name='bike_shop',
            field=models.ForeignKey(to='bike_aggregator.BikeShop'),
        ),
        migrations.AlterField(
            model_name='prices',
            name='rental_equipment',
            field=models.ForeignKey(to='bike_aggregator.RentalEquipment'),
        ),
    ]
