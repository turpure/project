# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-27 01:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='uid',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
