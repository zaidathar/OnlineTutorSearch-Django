from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User,Student,Tutor,Wallet,Bank
import datetime
class StudentSignUpForm(UserCreationForm):
    
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)


    class Meta(UserCreationForm.Meta):
        model = User
        fields=['username','email','password1','password2']
        
    @transaction.atomic
    def save(self):
        
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        
        user.save()
        wallet = Wallet(user=user)
        wallet.amount=2000.0    # for student bonus is given
        wallet.history.append(["**Bonus**","Credited",2000.0,str(datetime.datetime.now()).split(" ")[0]])
        wallet.save()
        student = Student.objects.create(user=user)
        student.contact="Phone Number"#self.cleaned_data.get('contact')
        student.location="Enter City Name"#self.cleaned_data.get('location')
        student.save()
        bank = Bank(user = user)
        bank.name = user.first_name +" "+user.last_name
        bank.account_number = "OTS"+user.username+"S"
        datetimes= str(datetime.datetime.now()).split(" ")
        date = datetimes[0]
        time = datetimes[1][:5]
        bank.amount = 10000.0
        bank.history.append(['Deposited',10000.0,date,time])
        bank.save()
        return user

class TutorSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields=['username','email','password1','password2']

    @transaction.atomic
    def save(self):
 
        user = super().save(commit=False)
        user.is_tutor = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        # user.username=user.email[:user.email.find('@')]
        user.save()
        
        wallet = Wallet(user=user)
        wallet.save()
        tutor = Tutor.objects.create(user=user)
        tutor.contact="Enter Phone Number"
        tutor.location="Enter City Name"
        tutor.save()
        bank = Bank(user = user)
        bank.name = user.first_name +" "+user.last_name
        bank.account_number = "OTS"+user.username+"T"
        datetimes= str(datetime.datetime.now()).split(" ")
        date = datetimes[0]
        time = datetimes[1][:5]
        bank.history.append(['Deposited',0.0,date,time])
        bank.save()
        return user


class ChatForm(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off'}))
    
    