# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-24 21:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0012_auto_20180221_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default=None, upload_to=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
