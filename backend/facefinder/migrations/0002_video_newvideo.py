# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-09 16:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facefinder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='newVideo',
            field=models.FileField(default=None, upload_to='documents/'),
            preserve_default=False,
        ),
    ]
