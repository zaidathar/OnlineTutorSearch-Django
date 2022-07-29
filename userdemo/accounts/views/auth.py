from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import User,Tutor,Student,Bank,Wallet
from django.urls import reverse
from .mymethod import get_combination,get_valid_name
from accounts.forms import StudentSignUpForm,TutorSignUpForm
from django.http import HttpResponse,request
from django.template import RequestContext
import datetime
def login_request(request):
    print("Login_request")
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
      
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None :
                login(request,user)
                return redirect('/')
            else:
                messages.error(request,"Invalid username or password")
        else:
            print("Invalid form")
            for field in form.errors:
                print(field)
            print(messages.error(request,"Invalid username or password"))
    return render(request, '../templates/accounts/login.html',
    context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')

def bank_form(request,**kwargs):
    return render(request,"pages/bankFormPage.html")

def bank_auth(request):
    user_id = request.user.id
    user = User.objects.get(id = user_id)
    print("Inside auth")
    if request.POST:
        print("Inside Post auth")
        query_field = request.POST.dict()
        password = query_field['password']
        current_user = authenticate(username=user.username, password=password)
        account = query_field.get('account')
        
        if current_user is not None :
            customer = Bank.objects.get(account_number = account)
            context = {'customer':customer,"user_details":user}
            return render(request,"pages/bankPassbook.html",context)
        else:
            return redirect('bank_auth')
    else:
        return render(request,"pages/bankLogin.html")

def bank_details(request):
    return redirect('/')
    
def bank_request(request):
    user_id = request.user.id
    user = User.objects.get(id = user_id)

    if request.POST:
        print("Entered  into post")
        query_field = request.POST.dict()
        password = query_field['password']
        current_user = authenticate(username=user.username, password=password)
        account = query_field.get('account')
        amount = query_field.get('amount')
        if current_user is not None :
            customer = Bank.objects.get(account_number = account)
            datetimes = str(datetime.datetime.now()).split(" ")
            date = datetimes[0]
            time = datetimes[1][:5]
            if User.objects.get(id = user_id).is_student:
                customer.amount -= float(amount)
                customer.history.append([
                    'Withdraw',amount,date,time
                ])
                customer.save()
                wallet = Wallet.objects.get(user_id = user_id)
                wallet.history.append([account,"Credited",amount,str(datetime.datetime.now()).split(" ")[0]])
                wallet.amount += float(amount)
                wallet.save()

            else:
                customer.amount += float(amount)
                customer.history.append([
                    'Credited',amount,date,time
                ])
                customer.save()
                wallet = Wallet.objects.get(user_id = user_id)
                wallet.history.append([account,"Transfer",amount,str(datetime.datetime.now()).split(" ")[0]])
                
                wallet.amount -= float(amount)

                wallet.save()

            return redirect("user_profile")
            
    else:
        return redirect('bank_form')
        # return render(request,'pages/bankFormPage.html',context)
        
    

