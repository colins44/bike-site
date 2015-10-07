# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0003_auto_20151007_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='bikeshop',
            name='post_code',
            field=models.CharField(max_length=225, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='bikeshop',
            name='street',
            field=models.CharField(max_length=225, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='bikeshop',
            name='street_number',
            field=models.CharField(max_length=225, null=True, blank=True),
        ),
    ]
