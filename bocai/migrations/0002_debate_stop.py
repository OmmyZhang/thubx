# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-03-23 07:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bocai', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='debate',
            name='stop',
            field=models.BooleanField(default=False),
        ),
    ]
