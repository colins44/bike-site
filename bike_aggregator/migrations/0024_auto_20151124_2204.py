# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0023_auto_20151124_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockitem',
            name='stock_id',
            field=models.IntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reservation',
            name='shop_id',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='stockitem_id',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='stockitem',
            name='shop_id',
            field=models.IntegerField(db_index=True),
        ),
    ]
