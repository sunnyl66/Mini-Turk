# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-09 01:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turk', '0086_auto_20171208_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='bid_deadline',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 15, 20, 16, 7, 832727)),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_deadline',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 29, 20, 16, 7, 832727)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='acc_created',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 8, 20, 16, 7, 832727)),
        ),
    ]