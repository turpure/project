# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-28 00:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0015_auto_20160928_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='curdate',
            field=models.DateField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='starttime',
            field=models.DateField(default=False),
        ),
    ]
