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
        result = requests.get('http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=a5e7afca7c5950b7d739578c35e60ac9')
        data = result.json()
        context = {'first_name':request.user.first_name, 'humidity' : data['list'][0]['main']['humidity'], 'weather' : data['list'][0]['weather'][0]['description']}
        #context = {'weather' : data['list'][0]['weather'][0]['description']}
        return render(request, 'weather.html', context)
        return render(request,'dashboard.html',context)
    else:
        return redirect('home')

def weather(request):
	#gets data from open weather, from moscow
    result = requests.get('http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=a5e7afca7c5950b7d739578c35e60ac9')
    data = result.json()
    context = {'first_name':request.user.first_name, 'humidity' : data['list'][0]['main']['humidity'], 'weather' : data['list'][0]['weather'][0]['description']}
    #context = {'weather' : data['list'][0]['weather'][0]['description']}
    return render(request, 'weather.html', context)

def daily(request):
	return render(request, 'daily.html')


def myproducts(request):
	return render(request, 'myproducts.html')

'''
def myproducts(request):
    if request.user.is_authenticated:
        for p in request.user.product_set:
            if p.type == 'moisturizer':
                context = {'moisturizerName': p.name}
                context = {'moisturizerURL': p.URL}
            elif p.type == 'cleanser':
                context = {'cleanserName': p.name}
                context = {'cleanserURL': p.URL}
            elif p.type == 'sunCare':
                context = {'sunCareName': p.name}
                context = {'sunCareURL': p.URL}
    else:
        return redirect('home')
'''