from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(default=None, null=True)

def __str__(self):
    return self.user.username

class Item(models.Model):
    item = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Coode(models.Model):
    coode = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Daytrend(models.Model):
    daytrend = models.TextField()
    myimage = models.ImageField(upload_to='', blank=True, null=True)
    updatedate = models.DateTimeField(auto_now=True)

class Munthtrend(models.Model):
    munthtrend = models.TextField()
    myimage = models.ImageField(upload_to='', blank=True, null=True)
    updatedate = models.DateTimeField(auto_now=True)
    
class Notice(models.Model):
    notice = models.TextField()
    myimage = models.ImageField(upload_to='', blank=True, null=True)
    updatedate = models.DateTimeField(auto_now=True)

class Marking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    outfitscore = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    upper = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    lower = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    todaypoint = models.CharField(max_length=500)
    myimage = models.ImageField(upload_to='', blank=True, null=True)
    updatedate = models.DateTimeField(auto_now=True)

class Sns(models.Model):
    post= models.CharField(max_length=100)
    myimage = models.ImageField(upload_to='', blank=True, null=True)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    good = models.IntegerField(default=0)
    updatedate = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.post


