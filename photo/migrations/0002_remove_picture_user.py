# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-30 01:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picture',
            name='user',
        ),
    ]