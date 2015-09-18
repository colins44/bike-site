# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0002_bikesearch_no_of_bikes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bikesearch',
            name='no_of_bikes',
            field=models.IntegerField(),
        ),
    ]
