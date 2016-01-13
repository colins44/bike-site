# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0022_auto_20151214_0928'),
    ]

    operations = [
        migrations.AddField(
            model_name='bikeshop',
            name='fake',
            field=models.BooleanField(default=False),
        ),
    ]
