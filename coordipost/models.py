from django.db import models

# Create your models here.

class Account(models.Model):
    username = models.CharField(max_length=20)
    userid = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    birthday = models.DateField()
    email = models.EmailField()
    item = models.CharField(max_length=50)
    coode = models.CharField(max_length=50)

class Main(models.Model):
    deytrend = models.CharField(max_length=500)
    munthtrend = models.TextField()
    notice = models.TextField()

class Marking(models.Model):
    outfitscore = models.DecimalField()
    upper = models.DecimalField()
    lower = models.DecimalField()
    todeypoint = models.CharField(max_length=500)

class Sns(models.Model):
    post = models.CharField(max_length=100)


