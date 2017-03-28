#coding:utf-8
from __future__ import unicode_literals

from django.db import models

class Player(models.Model):
    name  = models.CharField(max_length=50)
    score = models.IntegerField(default=0)
    def __str__(self):
        return (self.name + ' : ' + str(self.score)).encode('utf-8')

class Betting(models.Model):
    player = models.CharField(max_length=50)
    team = models.CharField(max_length=50)
    num = models.IntegerField(default=0)
    odds = models.FloatField()
    def __str__(self):
        return (u'%s下注%s %s个菠菜，赔率%s' % (self.player,self.team,str(self.num),self.odds)).encode('utf-8')

class Debate(models.Model):
    team1 = models.CharField(max_length=50)
    odds1 = models.FloatField()
    team2 = models.CharField(max_length=50)
    odds2 = models.FloatField()
    def __str__(self):
        return ('%s(%s) vs %s(%s)' % (self.team1,str(self.odds1),self.team2,str(self.odds2))).encode('utf-8')
# Create your models here.