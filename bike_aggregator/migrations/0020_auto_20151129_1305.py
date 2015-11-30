# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0019_bikeshop_rental_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalequipment',
            name='slug',
            field=models.SlugField(max_length=225, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bikeshop',
            name='rental_options',
            field=models.ManyToManyField(to='bike_aggregator.RentalEquipment', blank=True),
        ),
    ]
