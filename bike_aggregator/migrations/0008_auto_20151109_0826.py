# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0007_auto_20151013_1302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bikesearch',
            name='bike_type',
        ),
        migrations.RemoveField(
            model_name='bikesearch',
            name='no_of_bikes',
        ),
        migrations.AddField(
            model_name='bikesearch',
            name='search_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
