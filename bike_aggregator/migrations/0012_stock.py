# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bike_aggregator', '0011_remove_bikeshop_rental_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=225)),
                ('last_change', models.DateTimeField(auto_now=True)),
                ('owned_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
    ]
