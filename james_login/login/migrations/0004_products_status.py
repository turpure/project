# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-28 05:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='status',
            field=models.CharField(default=0, max_length=2),
        ),
    ]
