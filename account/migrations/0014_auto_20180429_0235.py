# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-28 20:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_payment_paypal_confirmation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paypalconfirmation',
            name='ipn_message',
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
    ]
