# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-19 03:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='climateresina',
            name='pressao',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='climateresina',
            name='sensacao',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='climateresina',
            name='temperatura',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='climateresina',
            name='umidade',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='climateresina',
            name='vento',
            field=models.CharField(max_length=16),
        ),
    ]
