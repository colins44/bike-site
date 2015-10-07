# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0002_auto_20151005_1504'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentalEquipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=225)),
            ],
        ),
        migrations.RenameField(
            model_name='bikeshop',
            old_name='street',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='bikeshop',
            old_name='town',
            new_name='state',
        ),
        migrations.AddField(
            model_name='bikeshop',
            name='latitude',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=4),
        ),
        migrations.AddField(
            model_name='bikeshop',
            name='location',
            field=models.CharField(default='testng', max_length=225),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bikeshop',
            name='longitude',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='bikesearch',
            name='bike_type',
            field=models.CharField(max_length=225, choices=[(b'scooter', b'scooter'), (b'road_bike', b'road bike'), (b'mountain_bike', b'mountain bike'), (b'hybrid_bike', b'hybrid bike'), (b'touring_bike', b'touring bike'), (b'electric_bike', b'electric bike')]),
        ),
        migrations.AlterField(
            model_name='bikeshop',
            name='country',
            field=models.CharField(max_length=225, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='bikeshop',
            name='rental_options',
            field=models.ManyToManyField(to='bike_aggregator.RentalEquipment'),
        ),
    ]
