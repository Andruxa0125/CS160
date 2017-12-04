# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-04 00:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facefinder', '0003_auto_20171124_0136'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='video_frame_rate',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='video_height',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='video_number_of_frames',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='video_width',
            field=models.IntegerField(null=True),
        ),
    ]
