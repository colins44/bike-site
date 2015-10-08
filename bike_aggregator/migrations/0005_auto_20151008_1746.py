# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0004_auto_20151007_1709'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bikesearch',
            name='email',
        ),
        migrations.RemoveField(
            model_name='bikesearch',
            name='phone_number',
        ),
    ]
