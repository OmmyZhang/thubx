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
    if(1==1):
        debates = Debate.objects.all()
        p = Player.objects.get(name = request.user.username)
        haveBocai = p.score 

        fail = False
        succ = False
    
        if request.POST:
            bet = [0] * (2*debates.count())
            useBocai = 0
            
            for i in range(0,debates.count()):
                bet[2*i] = int(request.POST['t'+str(i)+'_l'])
                useBocai += bet[2*i]
                if bet[2*i] < 0:
                    fail = True

                bet[2*i+1] = int(request.POST['t'+str(i)+'_r'])
                useBocai += bet[2*i+1]
                if bet[2*i+1] < 0:
                    fail = True
                

            if useBocai > haveBocai:
                fail = True

            if not fail:

                p.score = haveBocai - useBocai
                p.save()

                for i in range(0,debates.count()):
                    if bet[2*i] > 0:
                        b =  Betting(
                                player = p.name,
                                team = debates[i].team1,
                                num = bet[2*i],
                                odds = debates[i].odds1,
                                )
                        b.save()
                        succ =True

                    if bet[2*i+1] > 0:
                        b =  Betting(
                                player = p.name,
                                team = debates[i].team2,
                                num = bet[2*i+1],
                                odds = debates[i].odds2,
                                )
                        b.save()
                        succ = True

        bettings = Betting.objects.filter(player=p.name)
        context = {
            "fail":fail,
            "succ":succ,
            "name":p.name,
            "have":p.score,
            "bettings":bettings,
            "debates":debates
            }
        return render(request,'bocai/betting.html',context)

def rank(request):
    ps = Player.objects.all().order_by("-score")
    return render(request,'bocai/rank.html',{"players":ps})

@staff_member_required
def manage(request):
    return 0
# Create your views here.
