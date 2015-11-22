# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bike_aggregator', '0015_auto_20151122_1209'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='name',
            new_name='make',
        ),
        migrations.AddField(
            model_name='stock',
            name='size',
            field=models.CharField(max_length=225, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='type',
            field=models.CharField(max_length=225, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='year',
            field=models.IntegerField(blank=True, null=True, choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016)]),
        ),
    ]
