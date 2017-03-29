from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate , login
from django.contrib.auth.models import User
from .models import Player,Betting,Debate
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request,'bocai/index.html')

@login_required
def betting(request):

#    if not request.user.is_authenticated:
#        return HttpResponseRedirect('/user/login/')

    return 0

def rank(request):
    ps = Player.objects.all().order_by("-score")
#    ps.sort(key = score)

    return render(request,'bocai/rank.html',{"players":ps})

@staff_member_required
def manage(request):
#    if request.user.is_staff:
#        return render(request,'bocai/manage.html')
#    else:
#        return HttpResponse('Not allowed.<a href="/user/login">Login as staff.</a>')
    return 0
# Create your views here.
