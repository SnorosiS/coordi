from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.db import IntegrityError,transaction
from .models import Account,Item,Coode,Daytrend,Munthtrend,Notice,Marking,Sns
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


# Create your views here.

@transaction.atomic
def signupview(request):
    if request.method == 'GET':
        #初回到達ページ
        return render(request, 'sign/signup.html', {})
    else:
        #ﾕｰｻﾞｰが登録するﾃﾞｰﾀPOSTでﾃﾞｰﾀを渡す
        username_data = request.POST['username_data']
        email_data = request.POST['email_data']
        password_data = request.POST['password_data']
        birthday_data = request.POST['birthday_data']
        item_data = request.POST['item_data']
        coode_data = request.POST['coode_data']
        #try内の処理を行う
        try:
            #userを作る
            user = User.objects.create_user(username_data,email_data,password_data)
            #user=userでDjangoの持っているuserにaccount、item、coodeが紐付く
            Account.objects.create(user=user, birthday=birthday_data)
            Item.objects.create(user=user, item=item_data)
            Coode.objects.create(user=user, coode=coode_data)
            #照会が成功しﾕｰｻﾞｰ登録完了したらsignin画面
            return redirect('signin')
        #照会が失敗しすでにﾕｰｻﾞｰがいる場合ﾒｯｾｰｼﾞを出しsignup画面
        except IntegrityError:
            return render(request, 'sign/signup.html', {'error': 'このﾕｰｻﾞｰはすでに登録されています。'})

def signinview(request):
    if request.method == 'GET':
        return render(request, 'sign/signin.html')
    else:
        username_data = request.POST['username_data']
        password_data = request.POST['password_data']
        #上記ﾃﾞｰﾀをﾃﾞｰﾀﾍﾞｰｽに照合（authenticate）
        user = authenticate(request,username=username_data,password=password_data)
        if user:
            login(request,user)
            return redirect('main')        
        else:
            #login失敗
            return render(request,'sign/signin.html', {'error': 'username,passwordが違います。'})

def signoutview(request):
    logout(request)
    return redirect('signin')
    

@login_required
def mainview(request):
    daytrend = Daytrend.objects.latest('updatedate' )
    munthtrend = Munthtrend.objects.latest('updatedate')
    notice = Notice.objects.latest('updatedate')
    object = Marking.objects.filter(user=request.user).latest('updatedate')
    return render(
        request,
        'main/main.html' ,
        { 'daytrend':daytrend,'munthtrend':munthtrend,'notice':notice , 'object':object}
    )



@login_required
def todayyouview(request):
    if request.method == 'POST':
        todaypoint= request.POST['todaypoint']
        myimage = request.FILES['myimage']
        Marking.objects.create(user=request.user, todaypoint=todaypoint, myimage=myimage)
        return redirect('todayyoumarking')
    return render(request, 'main/todayyou.html')

@login_required
def todayyoumarkingview(request):
    object = Marking.objects.filter(user=request.user).latest('updatedate')
    return render(request, 'main/todayyoumarking.html' , {'object':object})

@login_required
def snsview(request, marking_id=None):
    object=None
    if marking_id:
        object = Marking.objects.get(id=marking_id)
        
    if request.method == 'POST':
        post= request.POST['post']
        myimage = request.FILES['myimage']
        Sns.objects.create(user=request.user, post=post, myimage=myimage)
    return render(request, 'main/sns.html', {'object':object})


