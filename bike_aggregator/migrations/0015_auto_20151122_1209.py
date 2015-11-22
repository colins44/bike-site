# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0014_bikeshop_owned_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bikeshop',
            name='owned_by',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
