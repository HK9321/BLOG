# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-27 12:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='collectpost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField()),
                ('pid', models.IntegerField()),
            ],
        ),
    ]
