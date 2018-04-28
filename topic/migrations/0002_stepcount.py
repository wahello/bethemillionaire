# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-23 15:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StepCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step1', models.BooleanField(default=True)),
                ('step2', models.BooleanField(default=False)),
                ('step3', models.BooleanField(default=False)),
                ('step4', models.BooleanField(default=False)),
                ('step5', models.BooleanField(default=False)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]