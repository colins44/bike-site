# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0023_bikeshop_fake'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bikeshop',
            name='latitude',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=4, blank=True),
        ),
        migrations.AlterField(
            model_name='bikeshop',
            name='location',
            field=models.CharField(max_length=225, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='bikeshop',
            name='longitude',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=4, blank=True),
        ),
    ]
