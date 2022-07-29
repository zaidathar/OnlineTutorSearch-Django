from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import User,Tutor,Student
from django.urls import reverse
from .mymethod import get_combination,get_valid_name
from accounts.forms import StudentSignUpForm,TutorSignUpForm
from django.http import HttpResponse,request
from django.template import RequestContext

def home(request):
    if request.user.is_authenticated:
        user_details = User.objects.filter(id = request.user.id)

        if request.user.is_tutor:
            return redirect("tutor/")
            
        else:
            return redirect("student/")            

    else:
        context={}
        return render(request,"pages/landingPage.html",context)
        # return render(request,"pages/dashboard.html",context)


def error(request):
    message = "User Not Found "
    return render(request,"error.html",{'message':message})


def dashboard(request):
    print()
    if request.user.is_authenticated:
        return render(request,"tutorsearchbar.html")
    else:
        return redirect("accounts/")

