# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-21 08:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_itbaccount'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='expired_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
