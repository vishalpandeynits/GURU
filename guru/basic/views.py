from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import SignUpForm
from django.contrib.auth import get_user_model
from django_email_verification import sendConfirm
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
#CreateclassForm, NoteForm, AssignmentForm, AnnouncementForm, SubjectForm 

def home(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        return render(request,'home.html')

@login_required
def homepage(request):
    #createclass
    if request.POST.get('join_key'):
        join_key = request.POST.get('join_key')
        classroom = Classroom.objects.get(unique_id=join_key)
        classroom.members.add(request.user)
    class_name=Classroom.objects.all().filter(members=request.user).exclude(teacher = request.user)
    if request.method=='POST':
        createclassform = CreateclassForm(request.POST or None)
        if createclassform.is_valid():
            classroom=createclassform.save(commit=False)
            classroom.members = request.user
            classroom.teacher = request.user
            classroom.save()
    else:
        createclassform = CreateclassForm()
    my_classes = Classroom.objects.all().filter(teacher=request.user)
    params={'createclassform':createclassform,'my_classes':my_classes,'class_name':class_name}
    return render(request,'homepage.html',params)

def signup(request):
    message = None
    if request.method == 'POST':
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            username= request.POST.get('username')
            email= request.POST.get('email')
            password = request.POST.get('password1')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            if User.objects.filter(email=email).exists():
                message = 'E-mail is already registered with us, try another one.'
                return render(request, 'registration/signup.html', {'form': form,'message':message})

            user = get_user_model().objects.create(username=username, password=password, email=email, first_name=first_name, last_name= last_name)
            sendConfirm(user)
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def subjects(request,unique_id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    form=None
    if request.user==classroom.teacher:
        if request.method=="POST": 
            form = SubjectForm(request.POST or None, request.FILES)
            if form.is_valid():
                subject=form.save(commit=False)
                subject.classroom=classroom
                subject.save()
        else:
            form = SubjectForm(request.POST or None, request.FILES)
    subjects = Subject.objects.all().filter(classroom=classroom)
    params = {'subjects':subjects,'form':form,'classroom':classroom}
    return render(request,'subjects.html',params)

@login_required
def subject_page(request,unique_id,subject_id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    params = {'subject':subject,'classroom':classroom}   
    return render(request,'subject_page.html',params)
