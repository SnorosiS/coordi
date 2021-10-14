from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.db import IntegrityError,transaction
from .models import Account,Item,Coode,Daytrend,Munthtrend,Notice,Marking,Sns
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from google_cloud.vision_api import detect_safe_search
from .forms import UserForm, MarkingForm

# Create your views here.

@transaction.atomic 
#→データベーストランザクション・・・アカウント作成に失敗してデータベースに無駄なデータをつからないためのもの
def signupview(request):
    #→はじめ”GET”入ってきて、signinに入る
    if request.method == 'GET':
        form = UserForm()
        
        return render(request, 'sign/signup.html', {'form': form})
    else:
        form = UserForm(request.POST)
        #→ﾕｰｻﾞｰが登録するﾃﾞｰﾀPOSTでformにﾃﾞｰﾀを渡す
        if form.is_valid():
            #→formに送ったデータエラーがないか確認する
            username_data = form.cleaned_data['username']
            email_data = form.cleaned_data['email']
            password_data = form.cleaned_data['password']
            birthday_data = form.cleaned_data['birthday']
            #item_data = request.POST['item_data']
            #coode_data = request.POST['coode_data']
            #m→上記、バリデーションクリア後の綺麗なデータ。

            
            user = User.objects.create_user(username_data,email_data,password_data)
            #→formから帰ってきたクリーンデータでuserを作る
            Account.objects.create(user=user, birthday=birthday_data)
            #Item.objects.create(user=user, item=item_data)
            #Coode.objects.create(user=user, coode=coode_data)
            #→user=userでDjangoの持っているuserにaccount、item、coodeが紐付く
            return redirect('signin')
            #→照会が成功しﾕｰｻﾞｰ登録完了したらsignin画面
        else:
            return render(request, 'sign/signup.html', {'form': form})
            #→Userがアカウント作成に失敗した際ここを通る17行目とコードは一緒だがformの中が違う。

def signinview(request):
    if request.method == 'GET':
    #→はじめ”GET”入ってきて、signing入る
        return render(request, 'sign/signin.html')
        #→はじめは全て”GET”なのでsigninに入る
    else:
        username_data = request.POST['username_data']
        password_data = request.POST['password_data']
        user = authenticate(request,username=username_data,password=password_data)
        #→上記ﾃﾞｰﾀをﾃﾞｰﾀﾍﾞｰｽに照合（authenticate）
        if user:
            login(request,user)
            return redirect('main') 
            #→照合成功でmain画面に入る       
        else:
            return render(request,'sign/signin.html', {'error': 'username,passwordが違います。'})#←formsに移動したい
             #login失敗

def signoutview(request):
    logout(request)
    return redirect('signin')
    #→Djangoのlogout機能でsignout
    
@login_required
#→loginで成功で”login_required”を通過できる
def mainview(request):
    daytrend = Daytrend.objects.latest('updatedate' )#→latest：ラテスト・・・必須条件。必ずデータが入っているものということ
    munthtrend = Munthtrend.objects.latest('updatedate')
    notice = Notice.objects.latest('updatedate')
    #→daytrend、munthtrend、notice、は'updatedate'を見て最新のデータを持ってくる
    object_list = Marking.objects.filter(user=request.user)
    #→
    '''
    if object_list.exists():
        object = object_list.latest('updatedate')
    else:
        object=None
        '''
    object = object_list.latest('updatedate') if object_list.exists() else None
    #→
    return render(
        request,
        'main/main.html' ,
        { 'daytrend':daytrend,'munthtrend':munthtrend,'notice':notice , 'object':object}
    )
    #→



@login_required
#→loginで成功したが”login_required”を通過できる
def todayyouview(request):
    form = MarkingForm()
    #→
    if request.method == 'POST':
        form=MarkingForm(request.POST, request.FILES)
        #postでtodayyouはformにデータがいき、バリデーションが走る
        
        if form.is_valid():
            #→formに送ったデータエラーがないか確認する
            todaypoint= request.POST['todaypoint']
            myimage = request.FILES['myimage']
            #→バリデーションクリア後綺麗なデータ。
            object = Marking.objects.create(user=request.user, todaypoint=todaypoint, myimage=myimage)
            #→データベースにデータを格納
            safe_search = detect_safe_search(object.myimage.path)
            #→Google Cloud vision APIを使用するコマンド・・・不適切なコンテンツをサーチする
            print(safe_search)
            point = (0,0,5,10,15,20)
            outfitscore = 100-point[ safe_search['adult']]-point[safe_search['spoofed']]-point[safe_search['violence']]-point[safe_search['racy']]
            #→基本100からvision APIから帰ってきた値に付随する点数を減算
            object.outfitscore=outfitscore
            #→算出されたoutfitscoreをobjectに格納
            object.save()
            #→objectの作成
            return redirect('todayyoumarking')
            #→todayyoumarkingに飛ぶ
    return render(request, 'main/todayyou.html', {'form':form})
    #→ifの処理に失敗した時formのエラーを画面に出す。


@login_required
#→loginで成功したが”login_required”を通過できる
def todayyoumarkingview(request):
    object = Marking.objects.filter(user=request.user).latest('updatedate')
    #→todayyouで採点された最新データとってくる。（latest：ラテストがいるので必須。確実に最新データが格納せれていないといけない。）
    return render(request, 'main/todayyoumarking.html' , {'object':object})
    #→objectの格納されたデータをtodayyoumarking.htmlに渡し表示する
    
@login_required
#→loginで成功したが”login_required”を通過できる
def snsview(request, marking_id=None):
    #→marking_idを取得するする。なければスルー
    object=None
    
    if marking_id:
        object = Marking.objects.get(id=marking_id)
        #→marking_idをobjectに持ってくる
        
    if request.method == 'POST':
        #→もしPOSTでリクエストされた場合
        post= request.POST.get('todaypoint')
        #→postにtodaypointを持ってくる
        if marking_id:
            myimage = Marking.objects.get(id=marking_id).myimage
        else:
            myimage = request.FILES.get('myimage')
        Sns.objects.create(userid=request.user, post=post, myimage=myimage)
        return redirect('sns')
        
    sns_list = Sns.objects.filter(userid=request.user).order_by('-updatedate')
    return render(request, 'main/sns.html', {'object':object, 'sns_list':sns_list})


