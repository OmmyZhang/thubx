from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate , login, logout
from django.contrib.auth.models import User
from bocai.models import Player

def login_view(request):
    
    name_error = False
    passwd_error = False

    if request.GET and request.GET.has_key('error'):
        if request.GET['error'] == 'user':
            name_error = True
        if request.GET['error'] == 'password':
            passwd_error = True
    
    return render(request,'login.html',{"ne": name_error,"pe": passwd_error}) 

def check(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except :
        return HttpResponseRedirect('/accounts/login/')

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/bocai/')
    else:
        if User.objects.filter(username=username):
            return HttpResponseRedirect('/accounts/login?error=password')
        else:
            return HttpResponseRedirect('/accounts/login?error=user')

def register(request):

    ne = False
    ie = False

    if request.GET and request.GET.has_key('error'):
        if request.GET['error'] == 'missingInfo':
            ie = True
        if request.GET['error'] == 'userExist':
            ne = True

    return render(request,'register.html',{'ne':ne,'ie':ie});

def newUser(request):

    try:
        username = request.POST['username']
        realname = request.POST['realname']
        wechat   = request.POST['wechat']
        password = request.POST['password']
    except :
        return HttpResponseRedirect('/accounts/register?error=missingInfo')

    if  not (username and realname and wechat and password):
        return HttpResponseRedirect('/accounts/register?error=missingInfo')

    if User.objects.filter(username=username):
        return HttpResponseRedirect('/accounts/register?error=userExist')
    
    user = User.objects.create_user(username,None,password)
    user.last_name = realname
    user.first_name = wechat
    user.save()

    p = Player(name = username,score = 3500)
    p.save()


    login(request,user)
    return HttpResponseRedirect('/bocai/')
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
