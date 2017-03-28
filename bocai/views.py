from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate , login
from django.contrib.auth.models import User

def index(request):
    return render('/bocai/index.html')

def betting(request):
    return 0

def rank(request):
    return 0

def manage(request):
    return 0

# Create your views here.
