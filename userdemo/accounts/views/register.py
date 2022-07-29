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

def register(request):
    #print("Enter ")
    return render(request,"accounts/register.html")


class student_register(CreateView):
    #print("Inside Student_register")
    model = User
    form_class = StudentSignUpForm
    
    template_name = "accounts/student_register.html"
    success_url = '/accounts/'
        
    def form_valid(self, form):
        #print('happening2')
        user=form.save()
        login(self.request, user)
        # return redirect('/')
        return redirect('/profile_update/')
        
    def form_invalid(self, form):
        #print(form)
        # #print(form['password1'].value())
        # #print(form['password2'].value())
        #print("form is invalid")
        return HttpResponse(request,"form is invalid.. this is just an HttpResponse object")
        
    def get_success_url(self):
        #print("Inside get_Success_Url")
        pk = self.kwargs["pk"]
        return reverse("view-accounts", kwargs={"pk": pk})

    #print("@@@@@@@@@@@ student_register @@@@@@@@")


class tutor_register(CreateView):
    model = User
    form_class = TutorSignUpForm
    template_name = "accounts/tutor_register.html"
    success_url='/accounts/'
    print("@@@@@@@@@@@ tutor_register @@@@@@@@")

    def form_valid(self, form):
        print("##### Enter In Form Validation #####")
        user = form.save()
        login(self.request, user)
        return redirect('/profile_update/')
    
    def form_invalid(self, form):
        for field in form.errors:
            print(field)
        print("form is invalid")
        return HttpResponse(request,"form is invalid.. this is just an HttpResponse object")
