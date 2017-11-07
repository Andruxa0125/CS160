# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django imports
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# My Imports
from .forms import SignUpForm
from .forms import NewVideoForm
from .models import Video
from .final_program import run_video
from django.core.files import File
import time
import os

#TODO: change this path
ROOT_PATH = "/Users/RYaryy/Desktop/Fall2017/CS160/CS160/backend/"

@login_required(login_url="login/")
def home(request):
    videos = Video.objects.filter(uploader=request.user.id).order_by('-uploaded_at')

    if request.method == 'POST':
        form = NewVideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.uploader = request.user
            video.save()
            time.sleep(1)
            print(ROOT_PATH + video.video.url)
            #while not os.path.exists(file_path):
            run_video(ROOT_PATH + video.video.url)

            # TODO: change this path to include dynamic naming
            f = open('/Users/RYaryy/Desktop/Fall2017/CS160/CS160/backend/media/documents/RESULTS_FOLDER_NAME/result.mp4', "rb")
            django_file = File(f)
            video.newVideo.save("new_video.mp4", django_file, save=True)
    else:
        form = NewVideoForm()

    return render(request, 'home.html', {'form': form, 'videos': videos})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})