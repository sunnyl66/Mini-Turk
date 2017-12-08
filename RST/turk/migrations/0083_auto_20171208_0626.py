# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-08 06:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turk', '0082_auto_20171208_0326'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='desired_position',
            field=models.CharField(choices=[('Client', 'Client'), ('Developer', 'Developer')], default='Client', max_length=9),
        ),
        migrations.AlterField(
            model_name='job',
            name='bid_deadline',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 15, 6, 26, 28, 684983)),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_deadline',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 29, 6, 26, 28, 685019)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='acc_created',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 8, 6, 26, 28, 683474)),
        ),
    ]