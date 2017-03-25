from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate , login
from django.contrib.auth.models import User

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
        return HttpResponseRedirect('/user/login/')

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/bocai/my/')
    else:
        if User.objects.filter(username=username):
            return HttpResponseRedirect('/user/login?error=password')
        else:
            return HttpResponseRedirect('/user/login?error=user')

def register(request):

    return render(request,'register.html');

def newUser(request):

    print "New"
    try:
        username = request.POST['username']
        realname = request.POST['realname']
        wechat   = request.POST['wechat']
        password = request.POST['password']
    except :
        return HttpResponseRedirect('/user/register?error=missingInfo')

    if  not (username and realname and wechat and password):
        return HttpResponseRedirect('/user/register?error=missingInfo')

    return HttpResponseRedirect('/user/login')
        
