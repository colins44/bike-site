# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0016_auto_20151122_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='no_in_stock',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
