# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0017_stock_no_in_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_data', models.DateField()),
                ('end_data', models.DateField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.RemoveField(
            model_name='stock',
            name='no_in_stock',
        ),
        migrations.AddField(
            model_name='booking',
            name='items',
            field=models.ManyToManyField(to='bike_aggregator.Stock'),
        ),
    ]
