# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bike_aggregator', '0019_auto_20151123_2012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='items',
        ),
        migrations.AddField(
            model_name='booking',
            name='owned_by',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
