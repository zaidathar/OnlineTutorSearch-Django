from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import User,Tutor,Student,Order,Meeting
from django.urls import reverse
from .mymethod import get_combination,get_valid_name
from accounts.forms import StudentSignUpForm,TutorSignUpForm
from django.http import HttpResponse,request
from django.template import RequestContext

def tutor(request):
    
    user = request.user.id
    orders = Order.objects.filter(t_id = user,status='pending')
    print(orders,"Pending Orders")
    meetings = Meeting.objects.filter(t_id = user,t_status = 'active')
    o_count = orders.count()
    m_count = meetings.count()
    print(meetings)
    meetings = list(meetings)[:m_count-4:-1] if m_count>3 else meetings   #to display only four recent meeting on Dashboard
    orders = list(orders)[:o_count-4:-1] if o_count > 3 else orders      #to display only four recent order on Dashboard
    print(orders,"last 3 order",)
    print(meetings,"last 3 meeting")

    no_active_m = Meeting.objects.filter(t_id = user,s_status='active',t_status='active').count()
    no_request = Order.objects.filter(t_id = user,status="pending").count()
    no_completed_m = Meeting.objects.filter(t_id = user, t_status='done' ).count()
    print("o_count",o_count)
    user_details = User.objects.get(id = user)
    is_tutor=True
    details=Tutor.objects.filter(user_id = user)
    context={"is_tutor":is_tutor,"user_details":user_details,"details":details,
              "orders":orders,'meetings':meetings,"no_request":no_request,
              "no_active_m":no_active_m,"no_completed_m":no_completed_m,
              "o_count":o_count,"m_count":m_count
            }

    return render(request,"pages/dashboard.html",context)
    
def tutor_match(request):

    if request.POST:
        
        query_field = request.POST.dict()
        subject = query_field.get("subject")
        location = get_valid_name(query_field.get("location"))
        print("subject",)
        tutors = Tutor.objects.filter(subject__contains=[get_valid_name(subject)],location=location)
        print(tutors)
        if tutors.count()==0:
            
            subjects = get_combination(subject)
            print(subjects)
            for i in subjects:
                
                res = Tutor.objects.filter(subject__contains=[i],location=location)
                if res.count()!=0:
                    tutors=res
                    break
        
        after = {'visited':True}
        userdetail={}
        
        for i in range(tutors.count()):
            
            userdetail[i] = [User.objects.filter(id=tutors[i].user_id),tutors[i]]
         
        context = {"tutors":tutors,"after":after,'subject':subject,"userdetail":userdetail}
        return render(request,"tutor/tutorsearchbar.html",context) 

    return render(request,"tutor/tutorsearchbar.html")


def tutor_search(request):
    if not request.user.is_authenticated:
        return redirect("accounts/")
    
    return render(request,'tutor/tutorsearch.html')

