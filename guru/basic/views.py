from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse,Http404
from django.contrib.auth import get_user_model
from django_email_verification import sendConfirm
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def proper_pagination(object,index):
    start_index=0
    end_index=10
    if object.number>index:
        start_index = object.number-index
        end_index = start_index + end_index
    return (start_index,end_index)

def wrap_data(value):
    return "<div style='white-space:pre-line;'>"+value+"</div>"

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
            classroom.teacher = request.user
            classroom.save()
            classroom.members.add(request.user)
            classroom.save()
            # return redirect(f'/subject/{classroom.unique_id}')
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
    if request.user==classroom.teacher:
        if request.method=="POST": 
            form = SubjectForm(request.POST or None, request.FILES)
            if request.user==classroom.teacher:
                if form.is_valid():
                    subject=form.save(commit=False)
                    subject.classroom=classroom
                    subject.teacher = request.user.first_name + request.user.last_name
                    subject.save()

        else:
            form = SubjectForm()
    subjects = Subject.objects.all().filter(classroom=classroom)
    params = {
        'subjects':subjects,
        'form':form,
        'classroom':classroom
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
    notes = Note.objects.all().filter(subject_name=subject).order_by('-id')
    if request.GET.get('search'):
        search = request.GET.get('search')
        notes = notes.filter(Q(topic__icontains=search)|Q(description__icontains=search))

    if request.user==classroom.teacher:
        if request.method=="POST":
            form = NoteForm(request.POST,request.FILES)
            files = request.FILES.getlist('file')
            print(len(files))
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
        'page_range':page_range
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
    if request.user==classroom.teacher:
        if request.method=="POST":
            form = NoteForm(request.POST,request.FILES,instance=note)
            if form.is_valid():
                noteform = form.save(commit=False)
                noteform.subject_name = subject
                noteform.save()
                return redirect(f'/{unique_id}/{subject_id}/{note.id}/read')
        else:
            form= NoteForm(instance=note)
    else:
        Http404()
    params={
            'notes':notes,
            'subject':subject,
            'form':form,
            'classroom':classroom,
        }
    return render(request,'resources.html',params)

@login_required
def resource_delete(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    print(classroom.teacher)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    note = Note.objects.all().filter(subject_name=subject).get(id=id)
    if request.user == classroom.teacher:
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
    form = None
    if request.user == classroom.teacher:
        if request.method=="POST":
            form = AssignmentForm(request.POST,request.FILES)
            if form.is_valid():
                announcement = form.save(commit=False)
                announcement.subject_name = subject
                announcement.save()
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
        'page_range':page_range
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
    params={
        'assignment':assignment,
        'subject':subject,
        'classroom':classroom,
        'submissionform':form,
        'submission':submission
        }
    return render(request,'assignment_page.html',params)

@login_required
def assignment_update(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    assignment = Assignment.objects.all().filter(subject_name=subject).get(id=id)
    assignments = Assignment.objects.all().filter(subject_name=subject).order_by('submission_date').reverse()
    if request.user==classroom.teacher:
        if request.method=="POST":
            form = AssignmentForm(request.POST,request.FILES,instance=assignment)
            if form.is_valid():
                assignmentform = form.save(commit=False)
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
        }
    return render(request,'assignments.html',params)

@login_required
def assignment_delete(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    assignment = Assignment.objects.all().filter(subject_name=subject).get(id=id)
    if request.user==classroom.teacher:
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
    if request.method=="POST":
        form = AnnouncementForm(request.POST,request.FILES)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.subject_name = subject
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
            'page_range':page_range
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
    if request.user==classroom.teacher:
        if request.method=="POST":
            form = AnnouncementForm(request.POST,request.FILES,instance=announcement)
            if form.is_valid():
                announcementform = form.save(commit=False)
                announcementform.subject_name = subject
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
    if request.user==classroom.teacher:
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
        'members':members
    }
    return render(request,'thissubject.html',params)

@login_required
def delete_subject(request,unique_id, subject_id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    if request.user == classroom.teacher:
        subject.delete()
        return redirect(f'/{unique_id}/')
    else:
        raise Http404()

    params={
        'subject':subject,
        'classroom':classroom,
    }
    return render(request,'homepage.html',params)


