from django.db import models

# Create your models here.
class user(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=10,default="张三")
    phone = models.CharField(max_length=11,default="12300000000")
class DoubanTask(models.Model):
    username = models.CharField(max_length=20)
    taskname = models.CharField(max_length=20)
    status = models.CharField(max_length=20,default='')
    time = models.DateTimeField(auto_now_add=True,null=True)
    key = models.CharField(max_length=20,default='')
    type = models.CharField(max_length=20,default='')
    
class DoubanSubject(models.Model):
    taskid = models.IntegerField(default=1)
    subject = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    writer = models.CharField(max_length=1000)
    actors = models.CharField(max_length=1000)
    type = models.CharField(max_length=1000)
    date = models.CharField(max_length=1000)
    timelong = models.CharField(max_length=1000)
    IMDb = models.CharField(max_length=1000)
    text = models.TextField()
    score=models.FloatField(default=0.0)
    runtime=models.DateTimeField(auto_now_add=True,null=True)
    peoplenum=models.IntegerField(default=0)
    star_five=models.CharField(max_length=10,default="")
    star_four=models.CharField(max_length=10,default="")
    star_three=models.CharField(max_length=10,default="")
    star_two=models.CharField(max_length=10,default="")
    star_one=models.CharField(max_length=10,default="")
    district=models.CharField(max_length=10,default="")


    
    