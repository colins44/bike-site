# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0006_auto_20151008_1854'),
    ]

    operations = [
        migrations.AddField(
            model_name='bikesearch',
            name='city',
            field=models.CharField(max_length=225, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='bikesearch',
            name='country',
            field=models.CharField(max_length=225, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='bikesearch',
            name='latitude',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=4),
        ),
        migrations.AddField(
            model_name='bikesearch',
            name='longitude',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=4),
        ),
        migrations.AddField(
            model_name='bikesearch',
            name='post_code',
            field=models.CharField(max_length=225, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='bikesearch',
            name='state',
            field=models.CharField(max_length=225, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='bikesearch',
            name='street',
            field=models.CharField(max_length=225, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='bikesearch',
            name='street_number',
            field=models.CharField(max_length=225, null=True, blank=True),
        ),
    ]
