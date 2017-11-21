# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django imports
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.contrib.auth.models import User
import os

# My Imports
from .forms import SignUpForm
from .forms import NewVideoForm
from .models import Video

# Core imports
from .core.final_program import run_video

ROOT_PATH = "/Users/RYaryy/Desktop/Fall2017/CS160/CS160/backend/media/"
RESULT_VIDEO = "documents/RESULTS_FOLDER_NAME/result.mp4"

def home(request):
    return render(request, 'home.html')

@login_required
def login_redirect(request):
    return redirect('main', request.user.username, hash(hash(request.user.username)))

@login_required
def main(request, username, session_ID):
    videos = Video.objects.filter(uploader=request.user.id).order_by('-uploaded_at')
    if request.method == 'POST':
        form = NewVideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.uploader = request.user
            video.save()
            print(os.path.join(ROOT_PATH, str(video.video)))
            video_path = os.path.join(ROOT_PATH, str(video.video))
            run_video(video_path)
            result_video = os.path.join(ROOT_PATH, RESULT_VIDEO)
            f = open(result_video, "rb")
            django_file = File(f)
            video.newVideo.save("new_video.mp4", django_file, save=True)
    else:
        form = NewVideoForm()
    print(session_ID)
    return render(request, 'main.html', {'form': form, 'videos': videos})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main', request.user.username, abs(hash(hash(request.user.username))))
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
