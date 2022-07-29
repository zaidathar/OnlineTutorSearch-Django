from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import User,Tutor,Student,Order,Meeting
from django.urls import reverse
from .mymethod import get_combination,get_valid_name,slicing 
from accounts.forms import StudentSignUpForm,TutorSignUpForm
from django.http import HttpResponse,request
from django.template import RequestContext

def student(request):
    user_id = request.user.id
    user_details = User.objects.get(id = user_id)
    details = Student.objects.get(user_id = user_id)
    tutors = Tutor.objects.all()

    orders = Order.objects.filter(s_id= user_id,status = 'pending')

    meetings = Meeting.objects.filter(s_id = user_id, s_status = 'active')
    m_count = meetings.count()
    o_count = orders.count()
    print(o_count)
    
    meetings = list(meetings)[:m_count-4:-1] if m_count>3 else meetings   #to display only four recent meeting on Dashboard
    orders = list(orders)[:o_count-4:-1] if o_count > 3 else orders      #to display only four recent order on Dashboard
    print(meetings,"last 3 meeting")
    no_active_m = Meeting.objects.filter(s_id = user_id,s_status='active',t_status='active').count()
    no_request = Order.objects.filter(s_id = user_id,status="pending").count()
    no_completed_m = Meeting.objects.filter(s_id = user_id,s_status='done').count()

    context={"orders":orders,"user_details":user_details,"details":details,
              'tutors':tutors,'meetings':meetings,"no_request":no_request,
              "no_active_m":no_active_m,"no_completed_m":no_completed_m,
              "o_count":o_count,"m_count":m_count
            }
    return render(request,"pages/dashboard.html",context)
