# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0018_auto_20151123_1951'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='end_data',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='start_data',
            new_name='start_date',
        ),
    ]
