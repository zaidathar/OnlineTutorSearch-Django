from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render,HttpResponse
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import User,Tutor,Student,Wallet 
from django.urls import reverse
from .mymethod import get_combination,get_valid_name
from accounts.forms import StudentSignUpForm,TutorSignUpForm
from django.http import HttpResponse,request,response,JsonResponse
from django.template import RequestContext
from django.core import serializers
from django.contrib.auth.decorators import login_required

def profile_view(request,username):
    query_user = User.objects.filter(username = username)
    #print(query_user,"user")
    if not query_user:
        return redirect("/error")
    query_user = query_user[0]
    pk = query_user.id
    #print(pk,'pk')
    if query_user.is_student:
        details = Student.objects.get(user_id = pk )

    else:
        details = Tutor.objects.get(user_id = pk )

    context = {
        'query_user':query_user,
        'details':details
    }
    #print(context)
    return render(request,"pages/profilePage.html",context)



@login_required(login_url='/login/') #redirect when user is not logged in

def profile_update(request):
    #print("Entered in profile update")
    if request.POST:
        #print("Request to update profile")
        
        #print(request.POST)
        query_field = request.POST.dict()
        # #print(query_field,"ajax query field")
        first_name = get_valid_name(query_field.get("first_name"))
        last_name = get_valid_name(query_field.get("last_name"))
        contact = query_field.get("contact")
        location = get_valid_name(query_field.get("location"))
        dob = get_valid_name(query_field.get("dob"))
        gender = get_valid_name(query_field.get("gender"))
        img = request.FILES.get("profile_pic")
        #print(request.FILES,'Files')
        #print("Img selected",img)

        if request.user.is_tutor :
            # #print("yes tutor")
            subject = list(query_field.get("subject").split(','))
            rate = query_field.get("rate")
            day_availability = list(query_field.get("day_availability").split(','))
            expertise = query_field.get('expertise')
            bio = query_field.get("bio")
            
            tutor = Tutor.objects.get(user_id=request.user.id)
            # #print(tutor.__dict__)
            # #print(tutor.location,tutor.dob,tutor.gender,tutor.subject,tutor.rate,tutor.day_availability)
            tutor.contact=contact
            tutor.location=location
            tutor.dob=dob
            tutor.gender = gender
            tutor.subject=subject
            tutor.rate=rate
            tutor.day_availability=day_availability
            tutor.expertise = expertise
            tutor.bio = bio
            tutor.save()
            # #print(tutor.contact,tutor.location,tutor.dob,tutor.gender,tutor.subject,tutor.rate,tutor.day_availability)
            
        else:
            #print("Enter in Else")
            student = Student.objects.get(user_id=request.user.id)
            student.contact=contact
            student.location=location
            student.dob=dob
            student.gender=gender
            student.save()
        
        user = User.objects.get(id = request.user.id)
        
        user.first_name = first_name
        user.last_name = last_name
        if img != None:
            user.profile_pic=img
        user.save()
        
        
        return HttpResponse("")
        # return JsonResponse(serializers.serialize('json', response), safe=False)
    
    primary = User.objects.get(id = request.user.id)
    # #print(primary.profile_pic.url)
    if request.user.is_student:
        secondary = Student.objects.get(user_id=request.user.id)
        Dob = str(secondary.dob)
        arrays={'Dob':Dob}
    
    elif request.user.is_tutor:
        secondary = Tutor.objects.get(user_id=request.user.id)
        
        subjects =','.join(secondary.subject)
        #print(subjects,"sub")
        days = ','.join(secondary.day_availability)
        Dob = str(secondary.dob)
        arrays={"subjects":subjects,"days":days,'Dob':Dob}
    #print(Dob)    
    # form = TutorSignUpForm( instance = request.user)
    context = {"primary":primary,"secondary":secondary,"arrays":arrays}
    #print(arrays)
    return render(request,"pages/profile.html",context)


def user_profile(request):
    wallet = Wallet.objects.get(user_id = request.user.id)
    user = User.objects.get(id = request.user.id)
    if user.is_student:
        details = Student.objects.get(user_id = user.id)
    else:
        details = Tutor.objects.get( user_id = user.id)

    context = {'wallet':wallet,'user':user,'details':details}
    return render(request,"pages/userProfilePage.html",context)


def wallet_history(request):
    
    wallet = Wallet.objects.get(user_id = request.user.id).history
    print(wallet)
    #print(type(wallet[0]),wallet[0])
    return render(request,"accounts/walletHistory.html",{"wallet":wallet})