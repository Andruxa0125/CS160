# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django imports
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# My Imports
from forms import SignUpForm
from forms import NewVideoForm
from models import Video

@login_required(login_url="login/")
def home(request):
    videos = Video.objects.filter(uploader=request.user.id).order_by('-uploaded_at')

    if request.method == 'POST':
        form = NewVideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.uploader = request.user
            video.save()
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