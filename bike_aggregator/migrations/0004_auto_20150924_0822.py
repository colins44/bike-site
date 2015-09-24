# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.core.validators
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0003_auto_20150904_0800'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bikesearch',
            name='country',
        ),
        migrations.RemoveField(
            model_name='bikesearch',
            name='town_or_region',
        ),
        migrations.AddField(
            model_name='bikesearch',
            name='location',
            field=models.CharField(default=datetime.datetime(2015, 9, 24, 8, 22, 18, 131767, tzinfo=utc), help_text=b'where would you like to hire your bike?', max_length=225),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bikesearch',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]),
        ),
    ]
