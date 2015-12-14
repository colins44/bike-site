# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bike_aggregator', '0020_auto_20151129_1305'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('last_change', models.DateTimeField(auto_now=True)),
                ('owned_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shop_id', models.IntegerField(db_index=True)),
                ('stockitem_id', models.IntegerField(db_index=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('last_change', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='StockItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('owned_by', models.IntegerField(db_index=True)),
                ('stock_id', models.IntegerField(db_index=True)),
                ('type', models.CharField(max_length=225, null=True, blank=True)),
                ('make', models.CharField(max_length=225)),
                ('year', models.IntegerField(blank=True, null=True, choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016)])),
                ('size', models.CharField(max_length=225, null=True, blank=True)),
                ('last_change', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='stock',
            name='no_in_stock',
        ),
        migrations.AddField(
            model_name='booking',
            name='reservations',
            field=models.ManyToManyField(to='bike_aggregator.Reservation'),
        ),
    ]
