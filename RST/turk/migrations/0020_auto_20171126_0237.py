# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-26 02:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turk', '0019_profile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='M', max_length=1),
        ),
    ]
