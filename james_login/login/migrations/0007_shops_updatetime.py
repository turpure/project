# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-29 01:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_products_mysku'),
    ]

    operations = [
        migrations.AddField(
            model_name='shops',
            name='updatetime',
            field=models.DateTimeField(null=True),
        ),
    ]
