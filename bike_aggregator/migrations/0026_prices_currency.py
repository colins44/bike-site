# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0025_prices'),
    ]

    operations = [
        migrations.AddField(
            model_name='prices',
            name='currency',
            field=models.CharField(default=b'EUR', max_length=6, choices=[(b'EUR', b'EUR'), (b'USD', b'USD'), (b'GDP', b'GDP')]),
        ),
    ]
