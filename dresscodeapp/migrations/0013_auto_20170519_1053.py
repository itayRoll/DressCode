# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-19 07:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dresscodeapp', '0012_auto_20170517_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 19, 7, 53, 7, 76000, tzinfo=utc), editable=False),
        ),
    ]
