# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from skincare.forms import *
from django.http import HttpResponse, HttpResponseForbidden
from skincare.models import *
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import requests

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, 'home.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.age = form.cleaned_data.get('age')

            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def dashboard(request):
    if request.user.is_authenticated:
        context = {'first_name':request.user.first_name}
        return render(request,'dashboard.html',context)
    else:
        return redirect('home')

def weather(request):
	#gets data from open weather, from moscow
	result = requests.get('http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=a5e7afca7c5950b7d739578c35e60ac9')
	data = result.json()
	print data['list'][0]['main']['humidity']
	return render(request, 'weather.html')

def daily(request):
	return render(request, 'daily.html')
def myproducts(request):
	return render(request, 'myproducts.html')

