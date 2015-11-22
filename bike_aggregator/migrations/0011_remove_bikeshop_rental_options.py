# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0010_enquiryemail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bikeshop',
            name='rental_options',
        ),
    ]
