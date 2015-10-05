# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bikeshop',
            name='town_or_region',
        ),
        migrations.AddField(
            model_name='bikeshop',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]),
        ),
        migrations.AddField(
            model_name='bikeshop',
            name='street',
            field=models.CharField(max_length=225, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='bikeshop',
            name='town',
            field=models.CharField(max_length=225, null=True, blank=True),
        ),
    ]
