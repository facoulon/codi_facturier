# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-08 14:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('facturier', '0009_auto_20181008_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commandline',
            name='quotation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facturier.Quotation'),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='status',
            field=models.CharField(choices=[('PAID', 'Paid'), ('REVIVE', 'Revive'), ('WAITING', 'Waiting')], default='WAITING', max_length=15),
        ),
    ]
