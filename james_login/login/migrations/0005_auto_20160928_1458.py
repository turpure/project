# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-28 06:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_products_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='quantitysold',
            field=models.IntegerField(),
        ),
    ]
