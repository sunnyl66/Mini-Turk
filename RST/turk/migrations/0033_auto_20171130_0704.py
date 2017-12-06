# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-30 07:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turk', '0032_profile_interest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='published',
        ),
        migrations.AddField(
            model_name='job',
            name='bid_deadline',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 7, 7, 4, 14, 171471)),
        ),
    ]