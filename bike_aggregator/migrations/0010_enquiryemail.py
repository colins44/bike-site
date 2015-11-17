# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0009_newslettersubscibers'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnquiryEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_address', models.EmailField(max_length=254, null=True, blank=True)),
                ('body', models.TextField(null=True, blank=True)),
                ('bike_shop', models.ForeignKey(to='bike_aggregator.BikeShop', blank=True)),
            ],
        ),
    ]
