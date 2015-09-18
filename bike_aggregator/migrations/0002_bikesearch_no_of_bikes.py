# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bikesearch',
            name='no_of_bikes',
            field=models.IntegerField(default=1),
        ),
    ]
