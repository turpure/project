# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-10 01:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_auto_20161010_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kwproducts',
            name='mysku',
            field=models.CharField(max_length=2, null=True),
        ),
    ]
