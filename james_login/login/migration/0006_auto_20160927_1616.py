# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-27 08:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20160927_1010'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='categotyid',
            new_name='categoryid',
        ),
    ]
