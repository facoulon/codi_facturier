# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-18 12:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturier', '0011_auto_20181016_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.CharField(choices=[('PAID', 'Paid'), ('REVIVE', 'Revive'), ('WAITING', 'Waiting')], default='WAITING', max_length=15),
        ),
    ]
