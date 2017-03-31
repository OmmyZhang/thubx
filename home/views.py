from django.shortcuts import render
# Create your views here.


def index(request):
    
    name = request.user.username
    return render(request,'home/index.html',{"name":name})
