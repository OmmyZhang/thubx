from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate , login
from django.contrib.auth.models import User
from .models import Player,Betting,Debate
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required


def index(request):
    name = request.user.username
    return render(request,'bocai/index.html',{"name":name})

def update_odds(d):
    print('update: ' + str(d))
    bs1 = Betting.objects.filter(team=d.team1, debate_id=d.id)
    sum1 = 0
    for b in bs1:
        sum1 += b.num

    bs2 = Betting.objects.filter(team=d.team2)
    sum2 = 0
    for b in bs2:
        sum2 += b.num
    
    print(sum1,sum2)

    odds1 = 1 + (sum2+1000.0) / (sum1+1000)
    odds2 = 1 + (sum1+1000.0) / (sum2+1000)

    d.odds1 = odds1
    d.odds2 = odds2
    d.save()
    

@login_required
def betting(request):
   # try:
        debates = Debate.objects.filter(stop=False)
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
                    this_debate = False
                    if bet[2*i] > 0:
                        b =  Betting(
                                player = p.name,
                                team = debates[i].team1,
                                num = bet[2*i],
                                debate_id = debates[i].id,
                                )
                        b.save()
                        this_debate = True
                        succ =True

                    if bet[2*i+1] > 0:
                        b =  Betting(
                                player = p.name,
                                team = debates[i].team2,
                                num = bet[2*i+1],
                                debate_id = debates[i].id,
                                )
                        b.save()
                        this_debate = True
                        succ = True
                    
                    if this_debate:
                        update_odds(debates[i])

        bettings = Betting.objects.filter(player=p.name)
        context = {
            "fail":fail,
            "succ":succ,
            "name":p.name,
            "have":p.score,
            "bettings":bettings,
            "debates":debates
            }
        print(bettings)
        return render(request,'bocai/betting.html',context)
  #  except Exception as e:
  #      return HttpResponse(repr(e)+ '<br> something wrong.Try later or connect at tdxdxoz@gamil.com')

def rank(request):
    name = request.user.username
    ps = Player.objects.all().order_by("-score")
    unkown = [0] * ps.count()
    
    i=0
    for p in ps:
        his_betting = Betting.objects.filter(player=p.name)
        for bb in his_betting:
            unkown[i] += bb.num
        i += 1
    
    ps_all = [{}] * ps.count()
    for i in range(0,ps.count()):
        ps_all[i] = {"name":ps[i].name,"score":ps[i].score,"more":unkown[i]}

    return render(request,'bocai/rank.html',{"players":ps_all,"name":name,"uk":unkown})

@staff_member_required
def manage(request):
    for bb in Betting.objects.all():
        if not Player.objects.filter(name=bb.player):
            bb.delete()

    if request.POST:
        win_team = request.POST['winner']
        lose_team = request.POST['loser']

        if Debate.objects.filter(team1=win_team, team2=lose_team).exists():
            d = Debate.objects.get(team1=win_team, team2=lose_team)
            t1_win = True
        else:
            d = Debate.objects.get(team2=win_team,team1=lose_team)
            t1_win = False

        winner =Betting.objects.filter(team=win_team,debate_id=d.id)
        odds = d.odds1 if t1_win else d.odds2

        _winner = [0] * winner.count()
        i = 0
        for bb in winner:
            _winner[i] = bb 
            i += 1
            p = Player.objects.get(name=bb.player)
            p.score += int(bb.num * odds)
            p.save()
        winner.delete()

        loser = Betting.objects.filter(team=request.POST['loser']) 
        _loser = [0] * loser.count()
        i = 0
        for bb in loser:
            _loser[i] = bb
            i += 1
        loser.delete() 
        
        context = {
                "winner":_winner,
                "loser":_loser
                }
    else:
        context = {}

    return render(request,'bocai/manage.html',context)

# Create your views here.
