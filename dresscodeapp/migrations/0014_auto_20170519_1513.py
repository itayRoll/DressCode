# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-19 12:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dresscodeapp', '0013_auto_20170519_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 19, 12, 13, 45, 815000, tzinfo=utc), editable=False),
        ),
    ]
