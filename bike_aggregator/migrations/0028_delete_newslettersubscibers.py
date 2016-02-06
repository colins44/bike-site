# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0027_auto_20160118_0645'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NewsLetterSubscibers',
        ),
    ]
