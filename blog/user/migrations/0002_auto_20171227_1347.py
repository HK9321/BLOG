# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-27 05:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.BooleanField(default=True),
        ),
    ]
