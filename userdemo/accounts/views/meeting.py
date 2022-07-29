from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import User,Tutor,Student,Order,Meeting,Chat,Wallet
from django.urls import reverse
from .mymethod import get_combination,get_valid_name,remaining_day
from accounts.forms import StudentSignUpForm,TutorSignUpForm,ChatForm
from django.http import HttpResponse,request,JsonResponse
from django.template import RequestContext
import datetime
from collections import defaultdict

def get_date(date):
    s=date.split(" ")
    s[0]=s[0].replace("'","")
    
    date= s[0].split("-")
    date.reverse()
    time = s[1][:5]

    return ["/".join(date),time]



def Chat_dict(a):
    d=defaultdict(list)
    # #print(a.chat)
    for i in a.chat:
        if type(i)==str:
            i=i.strip('][').split(', ')
        #print('i',i)
        i[2]=i[2].replace("'","")
        date_time = get_date(i[0])
        date = date_time[0]
        i.append(date_time[1])
        
        l=[]
        l.append(int(i[1]))
        l.append(i[2])
        l.append(i[3])
        d[date].append(l)
    
    # for i in d:
    #     #print(i,end="->")
    #     for j in d[i]:
    #         #print(j,end=" ")
    #     #print()
    #     #print()
        
    return d

def send_msg_chatbox(request,pk):
    #print("Calling Ajax")
    if request.is_ajax():
        #print('Hello')
        
        message = request.POST['message']
        meeting = Meeting.objects.get(id = pk)

        chating = Chat.objects.get(meeting_id = meeting.id)
        chating.chat.append([str(datetime.datetime.now()),request.user.id,message])
        chating.save()
        return HttpResponse("")
    return HttpResponse("")

def meeting_chat(request,pk):
    meeting = Meeting.objects.get(id = pk)
    student = User.objects.get( id = meeting.s_id)
    tutor = User.objects.get( id = meeting.t_id)
    order = Order.objects.get( id = meeting.order_id)

    if request.user.is_tutor:
        other_user = student
    else:
        other_user = tutor
    
    chating = Chat.objects.get(meeting_id = meeting.id )
    is_on = True

    
    form = ChatForm(request.POST)
    

    if form.is_valid():
        print(type(form.cleaned_data))

        message = form.cleaned_data['message']
        print(form.cleaned_data)
        #print("hi form is valid")
        print("message is->",message)
        chating.chat.append([str(datetime.datetime.now()),request.user.id,message])
        chating.save()
        # chat_dict=Chat_dict(chating)
        form = ChatForm()
        context = {'form':form,'is_on':is_on,'meeting':meeting,'chating':chating,'student':student,'tutor':tutor,'order':order,'other_user':other_user}
        
        return render(request,"pages/meetingPage.html",context)

    else:
        #print("chat form is invalid")
        # for field in form.errors:
        #     #print(field)
        
        context = {'form':form,'is_on':is_on,'chating':chating,'meeting':meeting,'student':student,'tutor':tutor,'order':order,'other_user':other_user}
        return render(request,"pages/meetingPage.html",context)


def meeting_view(request,pk):
    meeting = Meeting.objects.get(id = pk)
    student = User.objects.get( id = meeting.s_id)
    tutor = User.objects.get( id = meeting.t_id)
    order = Order.objects.get( id = meeting.order_id)

    is_on = False

    chating = Chat.objects.get( meeting_id = meeting.id)

    context = {'is_on':is_on,'meeting':meeting,'student':student,"tutor":tutor,'order':order,"chating":chating}
    return render(request,'pages/meetingPage.html',context)


def delete_meeting(request,pk):
    print("delete_meeting")
    meeting = Meeting.objects.get( id = pk)
    user =request.user.id
    #print(user,meeting.t_id)
    if meeting.t_id == user:
        meeting.t_status = 'cancel'
        meeting.s_status = 'cancel'
        wallet = Wallet.objects.get( user_id = meeting.s_id)

        amount = Order.objects.get( id = meeting.order_id).amount
        #print("cancellation amount",amount)
        wallet.amount+=amount

        wallet.history.append([meeting.order_id,"Refunded",amount,str(datetime.datetime.now()).split(" ")[0]])
        
        wallet.save()
        sys_wallet = Wallet.objects.get( user_id = 1 ) # id of admin is 1
        sys_wallet.amount -= amount
        sys_wallet.history.append([meeting.order_id,"Refunded",amount,str(datetime.datetime.now()).split(" ")[0]])
        sys_wallet.save()


        meeting.save()
        return redirect('/')
    else:
        apmnt_date = Order.objects.get( id = meeting.order_id).apmnt_time
        #print("Apmnt_date",apmnt_date)
        if remaining_day(str(datetime.datetime.now()),apmnt_date):
            meeting.s_status = 'cancel'
            meeting.t_status = 'cancel'
            wallet = Wallet.objects.get( user_id = meeting.s_id)

            amount = Order.objects.get( id = meeting.order_id).amount

            wallet.amount+=amount

            wallet.history.append([meeting.id,"Refunded",amount,str(datetime.datetime.now()).split()[0]])
            wallet.save()
            sys_wallet = Wallet.objects.get( user_id = 1 ) # id of admin is 1
            sys_wallet.amount -= amount
            sys_wallet.history.append(["order "+str(meeting.order_id),"Refunded",amount,str(datetime.datetime.now()).split(" ")[0]])
            sys_wallet.save()
            meeting.save()

            return redirect('/')

        else:
            error_message = "Cancel meeting before 1 day now request tutor to cancel"
            student = Student.objects.get(user_id = user)
            tutor = Tutor.objects.get(user_id = meeting.t_id)
            order = Order.objects.get( id = meeting.order_id)
            is_on = True

            context = {'is_on':is_on,'meeting':meeting,'student':student,"tutor":tutor,'order':order,'error_message':error_message}

            return render(request,'pages/meetingPage.html',context)
    




def create_meeting(request,pk):
    order = Order.objects.get(id = pk)

    order_id = order.id
    s_id = order.s_id
    t_id = order.t_id
    
    meeting = Meeting.objects.create(order_id = order_id , s_id = s_id , t_id = t_id )
    chat = Chat(meeting=meeting)
    chat.save()
    return redirect("/")




def meeting_complete(request,pk):
    #print("Meeting Completed")
    user = User.objects.get( id = request.user.id)
    meeting = Meeting.objects.get( id = pk )
    #print(user.is_student,"is_student")
    if user.is_student:
        meeting.s_status ="done"
        meeting.t_status ='done'
        meeting.save()
        order = Order.objects.get( id = meeting.order_id )

        tutor = Tutor.objects.get(user_id = meeting.t_id )
        tutor.students.append(meeting.s_id)
        tutor.no_of_hours += order.duration
        tutor.save()
        
        amount = (order.amount)*0.80  # 20% service charge deducted 
        t_wallet = Wallet.objects.get(user_id = meeting.t_id)
        t_wallet.amount += amount
        t_wallet.history.append(["Order "+str(order.id),'Credited',amount,str(datetime.datetime.now()).split()[0]])
        t_wallet.save()

        sys_wallet = Wallet.objects.get( user_id = 1 ) # id of admin is 1
        sys_wallet.amount -= amount
        sys_wallet.history.append(["Order "+str(order.id),"Transfered",amount,str(datetime.datetime.now()).split(" ")[0]])
        sys_wallet.save()
        
        return redirect("/")


def all_meeting(request):
    user_id = request.user.id
    if User.objects.get( id = user_id).is_tutor:

        meetings = Meeting.objects.filter( t_id = user_id)

    else:
        meetings = Meeting.objects.filter( s_id = user_id)

    context ={
        'meetings':meetings,
        'is_orders':False
    }
    return render(request,'pages/allDetails.html',context)