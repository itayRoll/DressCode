# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-01 15:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dresscodeapp', '0006_auto_20170413_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='items_not_as_pic',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='fuser',
            name='spammer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='fuser',
            name='spammer_credit',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='items_not_as_pic',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='clothingitem',
            name='question_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='fuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 1, 15, 39, 5, 620000, tzinfo=utc), editable=False),
        ),
    ]
