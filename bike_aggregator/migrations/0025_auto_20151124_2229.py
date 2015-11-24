# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0024_auto_20151124_2204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockitem',
            old_name='shop_id',
            new_name='owned_by',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='owned_by',
        ),
    ]
