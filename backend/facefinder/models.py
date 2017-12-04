# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Video(models.Model):
    video = models.FileField(upload_to='documents/')
    newVideo = models.FileField(upload_to='documents/', null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    video_number_of_frames = models.IntegerField(null=True)
    video_height = models.IntegerField(null=True)
    video_width = models.IntegerField(null=True)
    video_frame_rate = models.DecimalField(null=True, max_digits=5, decimal_places=2)