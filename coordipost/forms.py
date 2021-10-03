from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
 
 
class UserForm(forms.Form):
    username = forms.CharField(
        label='', max_length=100,
        help_text='◆[username]はCOORDIに於けるあなたを特定するIDです。ログイン時使用します。◆',     
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
    )
    password = forms.CharField(
        label='', max_length=100,
        help_text='◆[password]はCOORDIに於けるセキュリティの一つです。ログイン時使用します。◆',     
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}),
    )
    birthday = forms.DateField(
        label='',
        help_text='◆[生年月日]はあなたの生年月日です。passwordリセットなどに使います。◆',     
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'width:200px'}),
    )
    email = forms.EmailField(
        label='', max_length=100,
        help_text='◆[e-mail]はCOORDIからのお知らせや、passwordリセットなどに使います。◆',     
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'e-mail'}),
    )
    item = forms.MultipleChoiceField(
        label='', required=False,
        help_text='◆COORDIにあなたの好きなアイテムを教えてください。◆',
        choices=[(1, '帽子')],
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
    )
    coode = forms.MultipleChoiceField(
        label='', required=False,
        help_text='◆COORDIにあなたの好きなコーディネイトを教えてください。◆',
        choices=[(1, 'カジュアル')],
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).count():
            raise ValidationError('重複する名前があります')
            #self.add_error('username', '重複する名前があります')
        return username
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count():
            #self.add_error('email', '重複するメールアドレスがあります')
            raise ValidationError('重複するメールアドレスがあります')
        return email

    
    
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
    
    

