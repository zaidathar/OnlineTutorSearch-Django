from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import User,Tutor,Student,Order,Wallet
from django.urls import reverse
from .mymethod import get_combination,get_valid_name
from accounts.forms import StudentSignUpForm,TutorSignUpForm
from django.http import HttpResponse,request
from django.template import RequestContext
import datetime
def request_profile(request,pk):
    #print("Inside Request Profile ")
    order = Order.objects.get(id = pk)
    user = request.user.id
    is_tutor = User.objects.get(id = user).is_tutor
    
    if not is_tutor:
        user_info = Tutor.objects.get(user_id = order.t_id)
        user_basic = User.objects.get ( id = order.t_id) 
    
    else:
        user_info = Student.objects.get(user_id = order.s_id)
        user_basic = User.objects.get ( id = order.s_id)

    context = {'order':order,"user_basic":user_basic,"user_info":user_info,'is_tutor':is_tutor}

    return render(request,"pages/requestProfile.html",context) 

def request_view(request,username):
    #print(username,"inside request view")
    if request.POST:
        
        subject = request.POST.get('subject')
        duration = request.POST.get('duration')
        date = request.POST.get('date')
        message = request.POST.get('message')
        who = request.user.id
        whome = User.objects.get(username = username).id
        rate = Tutor.objects.get(user_id= whome).rate
        
        wallet = Wallet.objects.get(user_id = who)
        meeting_charge = float(rate)*float(duration)
        print("I am here ")
        if wallet.amount >= meeting_charge:
            print("Wallet had Excess Money")
            Order.objects.create(
                s_id=who,
                t_id=whome,
                apmnt_time=date,
                subject = subject,
                duration= float(duration),
                amount= meeting_charge,
                message = message
            )
            wallet.amount-=meeting_charge
            order_id = Order.objects.last().id
            wallet.history.append(["Order "+str(order_id),"Debited",meeting_charge,str(datetime.datetime.now()).split(" ")[0]])
            wallet.save()
            
            sys_wallet = Wallet.objects.get( user_id = 1 ) # id of admin is 1
            sys_wallet.amount += meeting_charge
            sys_wallet.history.append(["Order "+str(order_id),"Credited",meeting_charge,str(datetime.datetime.now()).split(" ")[0]])
            sys_wallet.save()

            return redirect("/")

        else:
            
            message = "Don't Have excess Money in wallet"
            tutor  = User.objects.get( username = username)
            
            return render(request,"pages/requestForm.html",{'message':message,'tutor':tutor}) 
            

        
    else:
        #print(username,"Username")
        tutor = User.objects.get(username = username)
        details = Tutor.objects.get(user_id = tutor.id)
        no_students = len(details.students)
        #print(tutor.first_name)
        no_hours = int(details.no_of_hours)
        context = {'tutor':tutor,'details':details,'no_hours':no_hours,"no_students":no_students}
        return render(request,'pages/requestForm.html',context)

def request_accepted(request,pk):
    #print("request_Accepted")
    order = Order.objects.get(id = pk )
    order.status = "done"
    order.save()

    return redirect("create_meeting",pk = pk)


def request_delete(request,pk):
    
    order = Order.objects.get(id = pk )
    amount = order.amount
    wallet = Wallet.objects.get(user_id = order.s_id)
    
    wallet.amount+=amount

    wallet.history.append(["Order "+str(order.id),"Refunded",amount,str(datetime.datetime.now()).split()[0]])
    wallet.save()
    sys_wallet = Wallet.objects.get( user_id = 1 ) # id of admin is 1
    sys_wallet.amount -= amount
    sys_wallet.history.append(["Order "+str(order.id),"Refunded",amount,str(datetime.datetime.now()).split(" ")[0]])
    sys_wallet.save()

    order.status="cancel"
    order.save()
    return redirect("/")


def all_request(request):
    user_id = request.user.id
    if User.objects.get( id = user_id).is_tutor:

        orders = Order.objects.filter( t_id = user_id)

    else:
        orders = Order.objects.filter( s_id = user_id)

    context ={
        'orders':orders,
        'is_orders':True
    }
    return render(request,'pages/allDetails.html',context)