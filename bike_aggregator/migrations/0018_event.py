# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0017_stock_no_in_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=225, null=True, blank=True)),
                ('data', models.TextField(null=True, blank=True)),
                ('event_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
