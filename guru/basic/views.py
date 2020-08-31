from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse,Http404
from django.contrib.auth import get_user_model
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage,send_mail
from .token import account_activation_token
import datetime

def proper_pagination(object,index):
    start_index=0
    end_index=10
    if object.number>index:
        start_index = object.number-index
        end_index = start_index + end_index
    return (start_index,end_index)

def home(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        return render(request,'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('login')
            # user.is_active = False
            # user.save()
            # current_site = get_current_site(request)
            # message = render_to_string('acc_active_email.html', {
            #     'user': user, 'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })
            # # Sending activation link in terminal
            # # user.email_user(subject, message)
            # mail_subject = 'Activate your account.'
            # to_email = form.cleaned_data.get('email')
            # email = send_mail(mail_subject, message,'vishalpandeynits@gmail.com',[to_email])
            # if email==0:
            #     return HttpResponse('Error in sending confirmation email')
            # # return HttpResponse('Please confirm your email address to complete the registration.')
            # return render(request, 'acc_activate_sent.html')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'signupform': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
        
@login_required
def homepage(request):
    if request.POST.get('join_key'):
        join_key = request.POST.get('join_key')
        classroom = Classroom.objects.get(unique_id=join_key)
        classroom.members.add(request.user)
    class_name=Classroom.objects.all().filter(members=request.user).exclude(teacher = request.user)
    if request.method=='POST':
        createclassform = CreateclassForm(request.POST or None)
        if createclassform.is_valid():
            classroom=createclassform.save(commit=False)
            classroom.created_by = request.user
            classroom.save()
            classroom.teacher.add(request.user)
            classroom.save()
            classroom.members.add(request.user)
            classroom.save()
            return redirect(f'/subject/{classroom.unique_id}')
    else:
        createclassform = CreateclassForm()
    my_classes = Classroom.objects.all().filter(teacher=request.user)
    params={
        'createclassform':createclassform,
        'my_classes':my_classes,
        'class_name':class_name
        }
    return render(request,'homepage.html',params)

@login_required
def subjects(request,unique_id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    is_teacher = Classroom.objects.filter(teacher=request.user).exists()
    form = None
    if request.method=="POST" and is_teacher: 
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject=form.save(commit=False)
            subject.classroom=classroom
            subject.teacher = request.user.first_name + request.user.last_name
            subject.save()
    else:
        if is_teacher:
            form = SubjectForm()
    subjects = Subject.objects.all().filter(classroom=classroom)
    members = classroom.members.all()
    teachers = classroom.teacher.all()
    students = members.difference(teachers)
    params = {
        'subjects':subjects,
        'form':form,
        'classroom':classroom,
        'students':students,
        'teachers':teachers,
        'is_teacher':is_teacher
        }
    return render(request,'subjects.html',params)

@login_required
def subject_page(request,unique_id,subject_id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    announcements = Announcement.objects.all().filter(subject_name=subject)
    params = {'subject':subject,'classroom':classroom,'announcements':announcements,}   
    return render(request,'subject_page.html',params)

@login_required
def resource(request,unique_id,subject_id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    is_teacher = Classroom.objects.filter(teacher=request.user).exists()
    notes = Note.objects.all().filter(subject_name=subject).order_by('-id')
    if request.GET.get('search'):
        search = request.GET.get('search')
        notes = notes.filter(Q(topic__icontains=search)|Q(description__icontains=search))
    form = None
    if request.method=="POST" and classroom.created_by==request.user:
        form = NoteForm(request.POST,request.FILES)
        files = request.FILES.getlist('file')
        data = Note()
        topic = request.POST.get('topic')
        description = request.POST.get('description')
        if form.is_valid():
            data.topic = topic
            data.description = "<pre>" + description + "</pre>"
            data.subject_name = subject
            for f in files:
                data.file = f
            data.save()
    else:
        if is_teacher:
            form= NoteForm()

    paginator = Paginator(notes,6)
    page_num=1
    if request.GET.get('page'):
        page_num = request.GET.get('page')
    query = paginator.page(page_num)
    start_index,end_index = proper_pagination(query,index=4)
    page_range = list(paginator.page_range)[start_index:end_index]
    params={
        'form':form,
        'subject':subject,
        'classroom':classroom,
        'notes':notes,
        'page':query,
        'page_range':page_range,
        'is_teacher':is_teacher
        }
    return render(request,'resources.html',params)

@login_required
def read_note(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    note = Note.objects.all().filter(subject_name=subject).get(id=id)
    params={
        'note':note,
        'subject':subject,
        'classroom':classroom,
        }
    return render(request,'read_note.html',params) 

@login_required
def resource_update(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    notes = Note.objects.all().filter(subject_name=subject)
    note = Note.objects.all().filter(subject_name=subject).get(id=id)
    form = None
    if classroom.created_by==request.user:
        if request.method=="POST":
            form = NoteForm(request.POST,request.FILES,instance=note)
            if form.is_valid():
                noteform = form.save(commit=False)
                noteform.subject_name = subject
                noteform.save()
                return redirect(f'/{unique_id}/{subject_id}/{note.id}/read')
        else:
            note.description = note.description[5:-6]
            form= NoteForm(instance=note)
    else:
        Http404()
    params={
            'notes':notes,
            'subject':subject,
            'form':form,
            'classroom':classroom,
            'is_teacher':classroom.created_by==request.user,
        }
    return render(request,'resources.html',params)

@login_required
def resource_delete(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    print(classroom.teacher)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    note = Note.objects.all().filter(subject_name=subject).get(id=id)
    is_teacher = Classroom.objects.filter(teacher=request.user).exists()
    if classroom.created_by==request.user:
        note.delete()
        return redirect(f'/{unique_id}/{subject_id}/resource')
    else:
        Http404()
    params={
        'note':note,
        'subject':subject,
        'classroom':classroom,
        }
    return render(request,'read_note.html',params)

@login_required
def assignment(request,unique_id,subject_id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    form=None
    if classroom.created_by==request.user:
        if request.method=="POST":
            form = AssignmentForm(request.POST,request.FILES)
            description = "<pre>" + request.POST.get('description') + "</pre>"
            time= request.POST.get('submission_date')
            time= time.replace("T"," ")
            d = datetime.datetime.fromisoformat(time+":00")
            submission_date =d.strftime('%Y-%m-%d %H:%M:%S')
            if form.is_valid():
                assignment = form.save(commit=False)
                assignment.submission_date = submission_date
                assignment.subject_name = subject
                assignment.description = description
                assignment.save()
        else:
            form= AssignmentForm()
    assignments = Assignment.objects.all().filter(subject_name=subject).order_by('-id')
    if request.GET.get('search'):
        search = request.GET.get('search')
        assignments = assignments.filter(Q(topic__icontains=search)|Q(description__icontains=search))
    
    paginator = Paginator(assignments,6)
    page_num=1
    page_range = [i for i in range(1,paginator.num_pages+1)]
    if request.GET.get('page'):
        page_num = request.GET.get('page')
    query = paginator.page(int(page_num))
    assignments=query.object_list

    params={
        'form':form,
        'subject':subject,
        'classroom':classroom,
        'assignments':assignments,
        'page':query,
        'page_range':page_range,
        }
    return render(request,'assignments.html',params)  

@login_required
def assignment_page(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    assignment = Assignment.objects.all().filter(subject_name=subject).get(id=id)
    if request.method=="POST":
        form = SubmitAssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            data=form.save(commit=False)
            data.submitted_by=request.user
            data.assignment= assignment
            data.save()
    else:
        form = SubmitAssignmentForm()
    submission = None
    try:
        submission = Submission.objects.all().filter(assignment=assignment,submitted_by=request.user)
    except Submission.DoesNotExist:
        submission = None

    all_submissions = Submission.objects.all().filter(assignment=assignment)
    late_submissions = Submission.objects.all().filter(submitted_on__gt=assignment.submission_date)
    ontime_submissions = all_submissions.difference(late_submissions)
    params={
        'assignment':assignment,
        'subject':subject,
        'classroom':classroom,
        'submissionform':form,
        'submission':submission,
        'all_submissions':all_submissions,
        'late_submissions':late_submissions,
        'ontime_submissions':ontime_submissions,
        'is_teacher':classroom.created_by==request.user,
        }
    return render(request,'assignment_page.html',params)

@login_required
def assignment_update(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    assignment = Assignment.objects.all().filter(subject_name=subject).get(id=id)
    assignments = Assignment.objects.all().filter(subject_name=subject).order_by('submission_date').reverse()
    form = None
    if classroom.created_by==request.user:
        if request.method=="POST":
            form = AssignmentForm(request.POST,request.FILES,instance=assignment)
            if form.is_valid():
                assignmentform = form.save(commit=False)
                assignmentform.description = assignmentform.description[5:-6]
                assignmentform.subject_name = subject
                assignmentform.save()
                return redirect(f'/{unique_id}/{subject_id}/{assignment.id}/assignment')
        else:
            form= AssignmentForm(instance=assignment)
    else:
        Http404()
    params={
            'assignment':assignment,
            'subject':subject,
            'form':form,
            'classroom':classroom,
            'assignments':assignments,
            'is_teacher':is_teacher
        }
    return render(request,'assignments.html',params)

@login_required
def assignment_delete(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    assignment = Assignment.objects.all().filter(subject_name=subject).get(id=id)
    if classroom.created_by==request.user:
        assignment.delete()
        return redirect(f'/{unique_id}/{subject_id}/assignments/')
    else:
        Http404()
    params={
        'subject':subject,
        'classroom':classroom,
        'assignments':assignments,
    }
    return render(request,'assignments.html',params)

@login_required
def announcement(request,unique_id,subject_id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    form = None
    if classroom.created_by==request.user:
        if request.method=="POST":
            form = AnnouncementForm(request.POST,request.FILES)
            if form.is_valid():
                announcement = form.save(commit=False)
                announcement.subject_name = subject
                announcement.description = "<pre>"+ request.POST.get('description')+"</pre>"
                announcement.save()
        else:
            form= AnnouncementForm()
    announcements = Announcement.objects.all().filter(subject_name=subject).order_by('-id')
    if request.GET.get('search'):
        search = request.GET.get('search')
        announcements = announcements.filter(Q(subject__icontains=search)|Q(description__icontains=search))

    paginator = Paginator(announcements,6)
    page_num=1
    page_range = [i for i in range(1,paginator.num_pages+1)]
    print(page_range)
    if request.GET.get('page'):
        page_num = request.GET.get('page')
    query = paginator.page(int(page_num))
    announcements=query.object_list

    params={
            'form':form,
            'subject':subject,
            'classroom':classroom,
            'announcements':announcements,
            'page':query,
            'page_range':page_range,
        }
    return render(request,'announcement.html',params)

@login_required
def announcement_page(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    announcement = Announcement.objects.all().filter(subject_name=subject).get(id=id)
    params={
        'announcement':announcement,
        'subject':subject,
        'classroom':classroom
        }
    return render(request,'announcement_page.html',params)

@login_required
def announcement_update(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    announcement = Announcement.objects.all().filter(subject_name=subject).get(id=id)
    announcements = Announcement.objects.all().filter(subject_name=subject).order_by('issued_on').reverse()
    is_teacher = Classroom.objects.filter(teacher=request.user).exists()
    form = None
    if classroom.created_by==request.user:
        if request.method=="POST":
            form = AnnouncementForm(request.POST,request.FILES,instance=announcement)
            if form.is_valid():
                announcementform = form.save(commit=False)
                announcementform.subject_name = subject
                announcementform.description = announcementform.description[5:-6]
                announcementform.save()

                return redirect(f'/{unique_id}/{subject_id}/{announcement.id}/announcement/')
        else:
            form= AnnouncementForm(instance=announcement)
    else:
        Http404()
    params={
            'announcement':announcement,
            'subject':subject,
            'form':form,
            'classroom':classroom,
            'announcements':announcements,
        }
    return render(request,'announcement.html',params)

@login_required
def announcement_delete(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    announcement = Announcement.objects.all().filter(subject_name=subject).get(id=id)
    if classroom.created_by==request.user:
        announcement.delete()
        return redirect(f'/{unique_id}/{subject_id}/announcement/')
    else:
        Http404()
    params={
        'subject':subject,
        'classroom':classroom,
        'announcement':announcement,
    }
    return render(request,'announcements.html',params)

@login_required
def this_subject(request,unique_id, subject_id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    members = classroom.members.all()
    params={
        'subject':subject,
        'classroom':classroom,
        'members':members,
        'is_teacher':classroom.created_by==request.user,
    }
    return render(request,'thissubject.html',params)

@login_required
def delete_subject(request,unique_id, subject_id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    if classroom.created_by==request.user:
        subject.delete()
        return redirect(f'/subject/{unique_id}/')
    else:
        raise Http404()

    params={
        'subject':subject,
        'classroom':classroom,
    }
    return render(request,'homepage.html',params)

@login_required
def make_admin(request,unique_id,username):
    classroom = Classroom.objects.get(unique_id=unique_id)
    is_teacher = Classroom.objects.filter(teacher=request.user).exists()
    if is_teacher:
        classroom.teacher.add(User.objects.get(username=username))
        return redirect(f'/subject/{unique_id}')   
    else:
        raise Http404()

@login_required
def remove_admin(request,unique_id,username):
    classroom = Classroom.objects.get(unique_id=unique_id)
    is_teacher = Classroom.objects.filter(teacher=request.user).exists()
    if is_teacher:
        classroom.teacher.remove(User.objects.get(username=username))
        return redirect(f'/subject/{unique_id}')  
    else:
        raise Http404()

@login_required
def remove_member(request,unique_id,username):
    classroom = Classroom.objects.get(unique_id=unique_id)
    is_teacher = Classroom.objects.filter(teacher=request.user).exists()
    if is_teacher or request.user==User.objects.get(username=username):
        classroom.members.remove(User.objects.get(username=username))
        if request.user==User.objects.get(username=username):
            return redirect('/homepage/')  
        else:
            return redirect(f'/subject/{unique_id}')
    else:
        raise Http404()



