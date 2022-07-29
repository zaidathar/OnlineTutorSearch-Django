from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm
from .models import User , Student , Tutor
from django.urls import reverse
# from .forms import StudentSingUpForm , TutorSingUpForm
from .forms import StudentSignUpForm,TutorSignUpForm
from django.http import HttpResponse,request
from django.template import RequestContext
# Create your views here.

def get_valid_name(s):
    s=s.strip()
    l=s.split(" ")
    l=[i.capitalize() for i in l]
    return ' '.join(l)

def get_combination(s):
    # Deep Learning -> [DEEP LEARNING,,deep learning,dEEP lEARING]
    def upperInverse(s):
        l=s.split(" ")
        l=[i[0].lower()+i[1:].upper() for i in l ]
        return " ".join(l)

    l=[s.upper(),s.lower(),upperInverse(s)]
    return l
    
def home(request):
    if request.user.is_authenticated:
        user_details = User.objects.filter(id = request.user.id)

        if request.user.is_tutor:
            return redirect("tutor/")
            
        else:
            return redirect("student/")            

    else:
        context={}
        return render(request,"accounts/index.html",context)

def error(request):
    message = "User Not Found "
    return render(request,"error.html",{'message':message})


def tutor(request):
    print("Tutor")
    user_details = User.objects.filter(id = request.user.id)
    details=Tutor.objects.filter(user_id=request.user.id)
    context={"user_details":user_details,"details":details}
    return render(request,"accounts/index.html",context)

def student(request):
    user_details = User.objects.filter(id = request.user.id)
    details = Student.objects.filter(user_id=request.user.id)
    tutors = Tutor.objects.all()
    print(tutors)
    context={"user_details":user_details,"details":details,'tutors':tutors}
    return render(request,"accounts/index.html",context)

def register(request):
    print("Enter ")
    return render(request,"register.html")

class student_register(CreateView):
    print("Inside Student_register")
    model = User
    form_class = StudentSignUpForm
    
    template_name = "accounts/student_register.html"
    success_url = '/accounts/'
        
    def form_valid(self, form):
        print('happening2')
        user=form.save()
        login(self.request, user)
        # return redirect('/')
        return redirect('/profile_update/')
        
    def form_invalid(self, form):
        print(form)
        # print(form['password1'].value())
        # print(form['password2'].value())
        for field in form.errors:
            print(field)
        print("form is invalid")
        return HttpResponse(request,"form is invalid.. this is just an HttpResponse object")
        
         
    
    


    def get_success_url(self):
        print("Inside get_Success_Url")
        pk = self.kwargs["pk"]
        return reverse("view-accounts", kwargs={"pk": pk})

    print("@@@@@@@@@@@ student_register @@@@@@@@")

    
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


def login_request(request):
    print("Login_request")
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        for i in form:
            print(i.value())
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
    return render(request, '../templates/login.html',
    context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')


def dashboard(request):
    if request.user.is_authenticated:
        return render(request,"dashboard.html")
    else:
        return redirect("accounts/")

def tutor_search(request):
    if not request.user.is_authenticated:
        return redirect("accounts/")
    
    return render(request,'tutorsearch.html')

def profile_view(request,slug):
    user = User.objects.filter(username = slug)
    print(user,"user")
    if not user:
        return redirect("/error")
    user = user[0]
    pk = user.id
    print(pk,'pk')
    if user.is_student:
        details = Student.objects.get(user_id = pk )

    else:
        details = Tutor.objects.get(user_id = pk )

    context = {
        'user':user,
        'details':details
    }
    print(context)
    return render(request,"profilePage.html",context)

def tutor_match(request):
    print("Enter")
    if request.POST:
        query_field = request.POST.dict()
        subject = query_field.get("subject")
        location = get_valid_name(query_field.get("location"))
        print(location,"location")
        tutors = Tutor.objects.filter(subject__contains=[subject.capitalize()],location=location)
        
        if tutors.count()==0:
            
            subjects = get_combination(subject)
            print(subjects)
            for i in subjects:
                
                res = Tutor.objects.filter(subject__contains=[i],location=location)
                print("res->",res)
                print("location",location)
                if res.count()!=0:
                    tutors=res
                    break
        print("Here")
        print(tutors,"tutors",type(tutors))  
        after = {'visited':True}
        # userdetail=User.objects.filter(id = 0)
        userdetail={}
        for i in range(tutors.count()):
            
            userdetail[i] = [User.objects.filter(id=tutors[i].user_id),tutors[i]]
         
        print(userdetail,"<-")
        print(userdetail[0][0],userdetail[0][1].bio)
        context = {"tutors":tutors,"after":after,'subject':subject,"userdetail":userdetail}
        return render(request,"dashboard.html",context) 

    return render(request,"dashboard.html")

def request_view(request):
    if request.POST:
        return redirect("/")
    else:
        return render(request,'requestForm.html')
def profile_update(request):
    if request.POST:
        print("Request to update profile")
        print(request.POST)
        query_field = request.POST.dict()
        first_name = get_valid_name(query_field.get("first_name"))
        last_name = get_valid_name(query_field.get("last_name"))
        contact = query_field.get("contact")
        location = get_valid_name(query_field.get("location"))
        dob = get_valid_name(query_field.get("dob"))
        gender = get_valid_name(query_field.get("gender"))
        img = request.FILES.get("profile_pic")
        

        if request.user.is_tutor :
            # print("yes tutor")
            subject = list(query_field.get("subject").split(','))
            rate = query_field.get("rate")
            day_availability = list(query_field.get("day_availability").split(','))
            expertise = query_field.get('expertise')
            bio = query_field.get("bio")
            
            tutor = Tutor.objects.get(user_id=request.user.id)
            # print(tutor.__dict__)
            # print(tutor.location,tutor.dob,tutor.gender,tutor.subject,tutor.rate,tutor.day_availability)
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
            # print(tutor.contact,tutor.location,tutor.dob,tutor.gender,tutor.subject,tutor.rate,tutor.day_availability)
            
        else:
            print("Enter in Else")
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
            user.profile_pi=img
        user.save()
        
        return redirect('/')
    
    primary = User.objects.filter(id = request.user.id)
    print(primary[0].profile_pic.url)
    if request.user.is_student:
        secondary = Student.objects.filter(user_id=request.user.id)
        Dob = str(secondary[0].dob)
        arrays={'Dob':Dob}
    
    elif request.user.is_tutor:
        secondary = Tutor.objects.filter(user_id=request.user.id)
        
        subjects =','.join(secondary[0].subject)
        print(subjects,"sub")
        days = ','.join(secondary[0].day_availability)
        Dob = str(secondary[0].dob)
        arrays={"subjects":subjects,"days":days,'Dob':Dob}
    print(Dob)    
    # form = TutorSignUpForm( instance = request.user)
    context = {"primary":primary,"secondary":secondary,"arrays":arrays}
    print(arrays)
    return render(request,"profile.html",context)


# print(template_name)

    # def get(self, request, *args, **kwargs):
    #     self.user = request.user
    #     print('happening1')
    #     return super().get(request, *args, **kwargs)

    # def post(self , request , *args , **kwargs):
    #     self.user = request.user
    #     print("Inside Post")
    #     return super().post(request, *args , **kwargs)

# def form_valid(self, form):
    #     print("$$$$$$$ form_valid $$$$$$$")
    #     user = form.save()
    #     login(self.request, user)
    #     return redirect('accounts/')
    
    # def get_initial(self , *args , **kwargs):
    #     initial = super().get_initial(**kwargs)
    #     print("Inside get_initial")
    #     print(initial)
    #     initial['first_name'] = "Your First Name"
    #     initial['last_name'] = 'Your Last Name'
    #     initial['phone_number'] = 'Type your Number'
    #     initial['location'] = 'Your location'
    #     print(initial)
