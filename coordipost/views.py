from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.db import IntegrityError,transaction
from .models import Account,Item,Coode,Daytrend,Munthtrend,Notice,Marking,Sns
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from google_cloud.vision_api import detect_safe_search
from .forms import UserForm

# Create your views here.

@transaction.atomic
def signupview(request):
    if request.method == 'GET':
        #初回到達ページ
        form = UserForm()
        return render(request, 'sign/signup.html', {'form': form})
    else:
        #ﾕｰｻﾞｰが登録するﾃﾞｰﾀPOSTでﾃﾞｰﾀを渡す
        form = UserForm(request.POST)
        if form.is_valid():
            username_data = form.changed_data['username']
            email_data = form.changed_data['email_data']
            password_data = form.changed_data['password_data']
            birthday_data = form.changed_data['birthday_data']
            #item_data = request.POST['item_data']
            #coode_data = request.POST['coode_data']
            #try内の処理を行う
            try:
                #userを作る
                user = User.objects.create_user(username_data,email_data,password_data)
                #user=userでDjangoの持っているuserにaccount、item、coodeが紐付く
                Account.objects.create(user=user, birthday=birthday_data)
                #Item.objects.create(user=user, item=item_data)
                #Coode.objects.create(user=user, coode=coode_data)
                #照会が成功しﾕｰｻﾞｰ登録完了したらsignin画面
                return redirect('signin')
            #照会が失敗しすでにﾕｰｻﾞｰがいる場合ﾒｯｾｰｼﾞを出しsignup画面
            except IntegrityError:
                return render(request, 'sign/signup.html', {'error': 'このﾕｰｻﾞｰはすでに登録されています。'})
        else:
            return render(request, 'sign/signup.html', {'form': form})

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
        object = Marking.objects.create(user=request.user, todaypoint=todaypoint, myimage=myimage)
        safe_search = detect_safe_search(object.myimage.path)
        print(safe_search)
        point = (0,0,5,10,15,20)
        outfitscore = 100-point[ safe_search['adult']]-point[safe_search['spoofed']]-point[safe_search['violence']]-point[safe_search['racy']]
        object.outfitscore=outfitscore
        object.save()
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
        post= request.POST.get('todaypoint')
        if marking_id:
            myimage = Marking.objects.get(id=marking_id).myimage
        else:
            myimage = request.FILES.get('myimage')
        Sns.objects.create(userid=request.user, post=post, myimage=myimage)
        return redirect('sns')
        
    sns_list = Sns.objects.filter(userid=request.user).order_by('-updatedate')
    return render(request, 'main/sns.html', {'object':object, 'sns_list':sns_list})


