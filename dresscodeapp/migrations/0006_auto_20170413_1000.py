# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-13 07:00
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dresscodeapp', '0005_auto_20170412_2101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clothingitem',
            name='_type',
        ),
        migrations.AddField(
            model_name='clothingitem',
            name='pattern',
            field=models.CharField(choices=[('1', 'NONE'), ('2', 'STRIPES'), ('3', 'DOTS'), ('4', 'CHECKED')], max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='clothingitem',
            name='type',
            field=models.CharField(choices=[('1', 'TSHIRT'), ('2', 'SHIRT'), ('3', 'SHORT PANTS'), ('4', 'HAT'), ('5', 'SHOES'), ('6', 'HOODIE'), ('7', 'DRESS'), ('8', 'LONG PANTS'), ('9', 'SWIM SUIT'), ('10', 'SUIT'), ('11', 'PANTS'), ('12', 'SKIRT')], max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='clothing_items',
            field=models.ManyToManyField(to='dresscodeapp.ClothingItem'),
        ),
        migrations.AlterField(
            model_name='clothingitem',
            name='color',
            field=models.CharField(choices=[('1', 'BLUE'), ('2', 'RED'), ('3', 'BLACK'), ('4', 'WHITE'), ('5', 'PURPLE'), ('6', 'GREEN'), ('7', 'YELLOW'), ('8', 'BROWN'), ('9', 'GREY')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='fuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 13, 7, 0, 20, 329000, tzinfo=utc), editable=False),
        ),
    ]
