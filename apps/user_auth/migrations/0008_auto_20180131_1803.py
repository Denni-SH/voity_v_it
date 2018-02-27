# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-31 16:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0007_friendship2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendship1',
            name='friends',
        ),
        migrations.RemoveField(
            model_name='friendship1',
            name='user',
        ),
        migrations.RemoveField(
            model_name='friendship2',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='friendship2',
            name='following',
        ),
        migrations.DeleteModel(
            name='Friendship1',
        ),
        migrations.DeleteModel(
            name='Friendship2',
        ),
    ]