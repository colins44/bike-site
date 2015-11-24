# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.datetime_safe import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0020_auto_20151123_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='last_change',
            field=models.DateTimeField(default=datetime.now()),
            preserve_default=False,
        ),
    ]
