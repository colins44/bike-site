# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0008_auto_20151109_0826'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsLetterSubscibers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=225, null=True, blank=True)),
                ('email_address', models.EmailField(max_length=254)),
                ('subscribed', models.BooleanField(default=True)),
            ],
        ),
    ]
