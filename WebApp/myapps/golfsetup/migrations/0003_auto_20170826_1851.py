# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-26 18:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golfsetup', '0002_tournament_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='playersPerTeam',
            field=models.PositiveSmallIntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='rounds',
            field=models.PositiveSmallIntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='teams',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]