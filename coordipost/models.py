from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    birthday = models.DateField(default=None, null=True)

class Item(models.Model):
    item = models.CharField(max_length=50)
    accountid = models.ForeignKey(User, on_delete=models.CASCADE)

class Coode(models.Model):
    coode = models.CharField(max_length=50)
    accountid = models.ForeignKey(User, on_delete=models.CASCADE)

class Daytrend(models.Model):
    daytrend = models.CharField(max_length=500)
    updatedate = models.DateTimeField(auto_now=True)

class Munthtrend(models.Model):
    munthtrend = models.TextField()
    updatedate = models.DateTimeField(auto_now=True)
class Notice(models.Model):
    notice = models.TextField()
    updatedate = models.DateTimeField(auto_now=True)

class Marking(models.Model):
    outfitscore = models.DecimalField(max_digits=5, decimal_places=2)
    upper = models.DecimalField(max_digits=5, decimal_places=2)
    lower = models.DecimalField(max_digits=5, decimal_places=2)
    todeypoint = models.CharField(max_length=500)
    myimage = models.ImageField()
    updatedate = models.DateTimeField(auto_now=True)

class Sns(models.Model):
    post = models.CharField(max_length=100)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    good = models.IntegerField(default=0)
    updatedate = models.DateTimeField(auto_now=True)


