# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-04 13:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturier', '0004_auto_20181004_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='customer'),
        ),
    ]