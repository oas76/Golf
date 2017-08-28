# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=200)
    handicap = models.FloatField(default=20.0)


    def __str__(self):
        return self.name

class Tournament(models.Model):
    name = models.CharField(max_length=200,default='New Tournament')
    teams = models.PositiveSmallIntegerField(default=1)
    playersPerTeam = models.PositiveSmallIntegerField(default=2)
    rounds = models.PositiveSmallIntegerField(default=2)
    changeTeams = models.BooleanField(default=False)

    def __str__(self):
        return self.name
