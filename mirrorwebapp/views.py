# mirrorwebapp/views.py
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

def login(request):
    return render(request, 'login.html')

def index(request):
    return render(request, 'index.html')

def espejo(request):
    return render(request, 'espejo.html')