from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
 
 
class UserForm(forms.Form):
    username = forms.CharField(
        #→
        label='', max_length=100,
        #→上限100文字(CharFieldの上限設定)
        help_text='◆[username]はCOORDIに於けるあなたを特定するIDです。ログイン時使用します。◆', 
        #→usernameの説明書き    
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
        #→widgetはDjango簡単HTML表示機能
    )
    password = forms.CharField(
        label='', max_length=100,
        #→上限100文字(CharFieldの上限設定)
        help_text='◆[password]はCOORDIに於けるセキュリティの一つです。ログイン時使用します。◆', 
        #→passwordの説明書き     
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}),
        #→widgetはDjango簡単HTML表示機能
    )
    birthday = forms.DateField(
        label='',
        help_text='◆[生年月日]はあなたの生年月日です。passwordリセットなどに使います。◆',  
        #→biethdayの説明書き    
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'width:200px'}),
        #→widgetはDjango簡単HTML表示機能
    )
    email = forms.EmailField(
        label='', max_length=100,
        help_text='◆[e-mail]はCOORDIからのお知らせや、passwordリセットなどに使います。◆',  
        #→emaolの説明書き       
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'e-mail'}),
        #→widgetはDjango簡単HTML表示機能
    )
    item = forms.MultipleChoiceField(
        #→
        label='', required=False,
        help_text='◆COORDIにあなたの好きなアイテムを教えてください。◆',
        #→itemの説明書き 
        choices=[(1, '帽子')],
        #→リスト型でitemを表示
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        #→widgetはDjango簡単HTML表示機能
    )
    coode = forms.MultipleChoiceField(
         #→
        label='', required=False,
        help_text='◆COORDIにあなたの好きなコーディネイトを教えてください。◆',
         #→coordiの説明書き
        choices=[(1, 'カジュアル')],
        #→リスト型でcoordiを表示
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        #→widgetはDjango簡単HTML表示機能
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).count():
            raise ValidationError('重複する名前があります')
            #→もし同じusernameがあれば「ValidationError」で（）内のコメントを返す
            #self.add_error('username', '重複する名前があります')
        return username
        #→同じusernameがなければusernameを返す。
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count():
            raise ValidationError('重複するメールアドレスがあります')
            #→もし同じemailがあれば「ValidationError」で（）内のコメントを返す
            #self.add_error('email', '重複するメールアドレスがあります')
        return email
        #→同じemailがなければemailを返す。

    
    
class MarkingForm(forms.Form):
    todaypoint = forms.CharField(
        max_length=500, 
        label='今日のポイント',
        widget=forms.Textarea(attrs={ 'rows':3, 'class': 'form-control'}),
    )
    myimage = forms.ImageField(
        label='今日のあなた',
        widget=forms.FileInput(attrs={'class': 'form-control'}),
    )
    
    

