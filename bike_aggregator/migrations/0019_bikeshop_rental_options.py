# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0018_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='bikeshop',
            name='rental_options',
            field=models.ManyToManyField(to='bike_aggregator.RentalEquipment', null=True, blank=True),
        ),
    ]
