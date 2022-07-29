from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
import datetime

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='pics',default="user.png")


class Student(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , primary_key=True)
    contact = models.CharField(max_length=20,default="Phone Number")
    location = models.CharField(max_length=100,default="Enter City")
    dob = models.DateField(null=True,default=datetime.date(1985,10,12))
    gender = models.CharField(max_length=10,default="Gender")
    no_of_tutors = models.PositiveIntegerField(default=0)
    tutors_id = ArrayField(models.IntegerField(),default=list)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        print("Inside Get_Absolute_Url")
        return '/%s/' % self.user.id



class Tutor(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , primary_key=True)
    contact = models.CharField(max_length=20,default="Phone Number")
    location = models.CharField(max_length=100,default="Enter City Name")
    dob = models.DateField(null=True,default=datetime.date(1985,10,12))
    gender = models.CharField(max_length=10,default="Gender")
    day_availability = ArrayField(models.CharField(max_length=100,null=True),default=list)
    subject=ArrayField(models.CharField(max_length=100,null=True),default=list)
    rate = models.PositiveIntegerField(default=200)    
    expertise = models.TextField(max_length=2000,default="Enter your skill to highlight yourself")
    bio = models.TextField(max_length=2000,default="")
    students = ArrayField(models.IntegerField(),default=list)
    no_lesson = models.IntegerField(default=0)
    no_of_hours = models.FloatField(default=0.0)
    rating = models.BigIntegerField(default=0)
    no_rate = models.BigIntegerField(default=0)


    def __str__(self):
        return self.user.username

class Wallet(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    
    amount = models.FloatField(default=0.0)
    history = ArrayField(models.CharField(max_length=100),default=list)

    def __str__(self):
        return self.user.username+"'s wallet"

class Order(models.Model):
    STATUS =[
        ('done','done'),
        ('pending','pending'),
        ('cancel','cancel')
    ]
    s_id = models.IntegerField()
    t_id = models.IntegerField()
    apmnt_time = models.DateField()
    subject = models.CharField(max_length=1000)
    duration = models.FloatField()
    amount = models.FloatField()
    message = models.CharField(max_length=1000)
    status = models.CharField(max_length=10,choices=STATUS,default='pending')


    def __str__(self):
        return self.subject+" "+str(self.apmnt_time)


class Meeting(models.Model):
    T_STATUS =[
        ('active',"active"),
        ('done','done'),
        ('cancel','cancel')
    ]
    
    S_STATUS =[
        ('active',"active"),
        ('done','done'),
        ('cancel','cancel')
    ]
    
    order_id = models.IntegerField()
    s_id = models.IntegerField()
    t_id = models.IntegerField()
    s_status = models.CharField(max_length=10,choices=S_STATUS,default="active")
    t_status = models.CharField(max_length=10,choices=T_STATUS,default="active")

    def __str__(self):
        return str(self.id)#+" "+s_status+" "+t_status
    

class Chat(models.Model):
    meeting = models.OneToOneField(Meeting,on_delete=models.CASCADE,primary_key=True)
    is_active = models.BooleanField(default=True)
    chat = ArrayField(models.CharField(max_length=2000),default=list)

    def __str__(self):
        return str(self.meeting.id)



class Bank(models.Model):   # If you connect project to payment API remove this , this is temporary bank for doing transaction
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length = 20)
    account_number = models.CharField(max_length = 10 )

    amount = models.FloatField(default = 0.0)
    history = ArrayField(models.CharField(max_length=100),default=list)
    