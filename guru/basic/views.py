from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import Http404
from django.db.models import Q
from .forms import *
from .models import *
import string
from random import choice,randint

def unique_id():
    characters = string.ascii_letters + string.digits
    password =  "".join(choice(characters) for x in range(randint(8,12)))
    return password

def member_check(user,classroom):
    return classroom.members.all().filter(username=user.username)

def proper_pagination(object,index):
    start_index=0
    end_index=10
    if object.number>index:
        start_index = object.number-index
        end_index = start_index + end_index
    return (start_index,end_index)

def home(request):
    if request.user.is_authenticated:
        return redirect('/homepage/')
    else:
        return render(request,'home.html')
       
@login_required
def homepage(request):
    if request.POST.get('join_key'):
        join_key = request.POST.get('join_key')
        classroom = Classroom.objects.get(unique_id=join_key)
        if classroom.need_permission==True:
            classroom.pending_members.add(request.user)
        else:
            classroom.members.add(request.user)
    
    if request.method=='POST':
        createclassform = CreateclassForm(request.POST or None)
        if createclassform.is_valid():
            classroom=createclassform.save(commit=False)
            classroom.unique_id = unique_id()
            classroom.created_by = request.user
            classroom.save()
            classroom.teacher.add(request.user)
            classroom.members.add(request.user)
            return redirect(f'/guru/{classroom.unique_id}/')
    else:
        createclassform = CreateclassForm()
    my_classes = Classroom.objects.all().filter(members=request.user)
    params={
        'createclassform':createclassform,
        'my_classes':my_classes
        }
    return render(request,'homepage.html',params)

@login_required
def subjects(request, unique_id, form = None):
    classroom = Classroom.objects.get(unique_id=unique_id)
    if member_check(request.user,classroom):
        subjects = Subject.objects.all().filter(classroom=classroom)
        members = classroom.members.all()
        teachers = classroom.teacher.all()
        students = members.difference(teachers)
        pending_members = classroom.pending_members.all()
        message=False
        # creator of classroom can add a subject with its teacher
        if request.user==classroom.created_by:
            if request.method=="POST": 
                form = SubjectForm(request.POST)
                if form.is_valid():
                    subject=form.save(commit=False)
                    subject.classroom=classroom
                    try:
                        teacher = User.objects.get(username=request.POST.get('teacher'))
                        if not members.filter(username=teacher.username).exists():
                            message="This user is not a member of this class. Tell him to join this classroom first."
                        else:
                            subject.teacher = teacher
                            subject.save()
                            message="Subject added"
                            classroom.teacher.add(teacher)
                            return redirect(f'/guru/{unique_id}/')
                            
                    except User.DoesNotExist:
                        message= "No such User exists."
            else:
                form = SubjectForm()
        params = {
            'subjects':subjects,
            'form':form,
            'classroom':classroom,
            'students':students,
            'teachers':teachers,
            'is_teacher':classroom.created_by == request.user or Classroom.objects.filter(teacher=request.user).exists(),
             'message':message,
             'pending_members':pending_members
            }
        return render(request,'subjects.html',params)
    else:
        raise Http404()

@login_required
def subject_page(request,unique_id,subject_id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    if member_check(request.user,classroom):
        subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
        announcements = Announcement.objects.all().filter(subject_name=subject)
        params = {'subject':subject,'classroom':classroom,'announcements':announcements,}   
        return render(request,'subject_page.html',params)
    else:
        raise Http404()

@login_required
def resource(request,unique_id,subject_id,form = None):
    classroom = Classroom.objects.get(unique_id=unique_id)
    if member_check(request.user,classroom):
        subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
        notes = Note.objects.all().filter(subject_name=subject).order_by('-id')
        is_teacher = classroom.created_by==request.user or request.user==subject.teacher
        if request.GET.get('search'):
            search = request.GET.get('search')
            notes = notes.filter(Q(topic__icontains=search)|Q(description__icontains=search))
        
        if is_teacher:
            if request.method=="POST":
                form = NoteForm(request.POST,request.FILES)
                if form.is_valid():
                    data=form.save(commit=False)
                    data.subject_name = subject
                    data.uploaded_by = request.user
                    data.save() 
                    return redirect(f'/{unique_id}/{subject_id}/resource/')
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
            'page_range':page_range,
            'is_teacher':classroom.created_by==request.user or request.user==subject.teacher
            }
        return render(request,'resources.html',params)
    else:
        raise Http404()

@login_required
def read_note(request, unique_id, subject_id, id, form = None):
    classroom = Classroom.objects.get(unique_id=unique_id)
    if member_check(request.user,classroom):
        subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
        notes = Note.objects.all().filter(subject_name=subject)
        note = Note.objects.get(id=id)
        if request.user==subject.teacher or classroom.created_by==request.user:
            if request.method=="POST": 
                form = NoteForm(request.POST,request.FILES,instance=note)
                if form.is_valid():
                    form.save()
                    return redirect(f'/{unique_id}/{subject_id}/{id}/read/')
            else:
                form= NoteForm(instance=note)
        params={
                'notes':notes,
                'subject':subject,
                'updateform':form,
                'note':note,
                'classroom':classroom,
                'is_teacher':classroom.created_by==request.user or request.user==subject.teacher,
            }
        return render(request,'read_note.html',params)
    else:
        raise Http404()

@login_required
def resource_delete(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    note = Note.objects.all().filter(subject_name=subject).get(id=id)
    if classroom.created_by==request.user or subject.teacher==request.user:
        note.delete()
        return redirect(f'/{unique_id}/{subject_id}/resource/')
    else:
        raise Http404()
    params={
        'note':note,
        'subject':subject,
        'classroom':classroom,
        }
    return render(request,'read_note.html',params)

@login_required
def assignment(request ,unique_id, subject_id, form=None):
    classroom = Classroom.objects.get(unique_id=unique_id)
    if member_check(request.user,classroom):
        subject = Subject.objects.get(id=subject_id)
        if classroom.created_by==request.user or subject.teacher==request.user:
            if request.method=="POST":
                form = AssignmentForm(request.POST,request.FILES)
                time= request.POST.get('submission_date')
                if form.is_valid():
                    assignment = form.save(commit=False)
                    assignment.submission_date = time
                    assignment.subject_name = subject
                    assignment.assigned_by = request.user
                    assignment.save()
            else:
                form= AssignmentForm()
        assignments = Assignment.objects.all().filter(subject_name=subject).order_by('-id')
        search = request.GET.get('search')
        if search:
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
    else:
        raise Http404()

@login_required
def assignment_page(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    if member_check(request.user, classroom):
        subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
        assignments = Assignment.objects.all().filter(subject_name=subject).order_by('submission_date').reverse()
        assignment = Assignment.objects.all().filter(subject_name=subject).get(id=id)
        #update assignment
        updateform =None
        if classroom.created_by==request.user or request.user==subject.teacher:
            if request.method=="POST":
                updateform = AssignmentForm(request.POST,request.FILES,instance=assignment)
                if updateform.is_valid():
                    assignmentform = updateform.save(commit=False)
                    assignmentform.subject_name = subject
                    assignmentform.save()
                    return redirect(f'/{unique_id}/{subject_id}/{assignment.id}/assignment/')
            else:
                updateform= AssignmentForm(instance=assignment)
        #submitting assignment
        form=None
        if classroom.created_by !=request.user and request.user!=subject.teacher:
            if request.method=="POST":
                form = SubmitAssignmentForm(request.POST, request.FILES)
                if form.is_valid():
                    data=form.save(commit=False)
                    data.submitted_by=request.user
                    data.assignment= assignment
                    data.current_status = True
                    data.save()
                    assignment.submitted_by.add(request.user)
                    return redirect(f'/{unique_id}/{subject_id}/{assignment.id}/assignment/')
            else:
                form = SubmitAssignmentForm()
        #list of submissions
        try:
            submission = Submission.objects.all().filter(assignment=assignment,submitted_by=request.user)
        except Submission.DoesNotExist:
            submission = None

        all_submissions = Submission.objects.all().filter(assignment=assignment)
        late_submissions = Submission.objects.all().filter(submitted_on__gt=assignment.submission_date)
        ontime_submissions = all_submissions.difference(late_submissions)
        submitted,not_submitted= None,None
        is_teacher = classroom.created_by==request.user or request.user==subject.teacher
        params={
            'assignment':assignment,
            'subject':subject,
            'form':form,
            'updateform':updateform,
            'classroom':classroom,
            'submissionform':form,
            'submission':submission,
            'all_submissions':all_submissions,
            'late_submissions':late_submissions,
            'ontime_submissions':ontime_submissions,
            'is_teacher':is_teacher,
            }

        if is_teacher:          
            members = classroom.members.all()
            teachers = classroom.teacher.all()
            students = members.difference(teachers)
            submitted = assignment.submitted_by.all()
            not_submitted = students.difference(submitted)
            params['submitted']=submitted
            params['not_submitted']=not_submitted
        return render(request,'assignment_page.html',params)
    else:
        raise Http404()

@login_required
def assignment_delete(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    assignment = Assignment.objects.all().filter(subject_name=subject).get(id=id)
    if classroom.created_by==request.user or request.user==subject.teacher:
        assignment.delete()
        return redirect(f'/{unique_id}/{subject_id}/assignments/')
    else:
        raise Http404()
    params={
        'subject':subject,
        'classroom':classroom,
        'assignments':assignments,
    }
    return render(request,'assignments.html',params)

@login_required
def announcement(request, unique_id, subject_id):
    form = None
    classroom = Classroom.objects.get(unique_id=unique_id)
    if member_check(request.user, classroom):
        subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
        if classroom.created_by==request.user or request.user==subject.teacher:
            if request.method=="POST":
                form = AnnouncementForm(request.POST,request.FILES)
                if form.is_valid():
                    announcement = form.save(commit=False)
                    announcement.subject_name = subject
                    announcement.announced_by = request.user
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
                'is_teacher':classroom.created_by==request.user or request.user==subject.teacher
            }
        return render(request,'announcement.html',params)
    else:
        raise Http404()

@login_required
def announcement_page(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    form = None
    if member_check(request.user, classroom):
        subject = Subject.objects.get(id=subject_id)
        announcements = Announcement.objects.all().filter(subject_name=subject).order_by('issued_on').reverse()
        announcement = Announcement.objects.get(id=id)
        if classroom.created_by==request.user or request.user==subject.teacher:
            if request.method=="POST":
                form = AnnouncementForm(request.POST,request.FILES,instance=announcement)
                if form.is_valid():
                    announcementform = form.save(commit=False)
                    announcementform.subject_name = subject
                    announcementform.save()
                    return redirect(f'/{unique_id}/{subject_id}/{announcement.id}/announcement/')
            else:
                form= AnnouncementForm(instance=announcement)
        params={
            'announcement':announcement,
            'subject':subject,
            'updateform':form,
            'classroom':classroom,
            'is_teacher':classroom.created_by==request.user or request.user==subject.teacher,
            }
        return render(request,'announcement_page.html',params)
    else:
        raise Http404()

@login_required
def announcement_delete(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    announcement = Announcement.objects.all().filter(subject_name=subject).get(id=id)
    if classroom.created_by==request.user or request.user==subject.teacher:
        announcement.delete()
        return redirect(f'/{unique_id}/{subject_id}/announcement/')
    else:
        raise Http404()
    params={
        'subject':subject,
        'classroom':classroom,
        'announcement':announcement,
    }
    return render(request,'announcements.html',params)

@login_required
def this_subject(request,unique_id, subject_id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    if member_check(request.user, classroom):
        subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
        params={
            'subject':subject,
            'classroom':classroom,
            'is_teacher':classroom.created_by==request.user,
        }
        return render(request,'thissubject.html',params)
    else:
        raise Http404()

@login_required
def delete_subject(request,unique_id, subject_id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    if classroom.created_by==request.user:
        subject.delete()
        return redirect(f'/guru/{unique_id}/')
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
        return redirect(f'/guru/{unique_id}/')   
    else:
        raise Http404()

@login_required
def remove_admin(request,unique_id,username):
    classroom = Classroom.objects.get(unique_id=unique_id)
    is_teacher = Classroom.objects.filter(teacher=request.user).exists()
    if is_teacher and not request.user==classroom.created_by:
        classroom.teacher.remove(User.objects.get(username=username))
        return redirect(f'/guru/{unique_id}/')  
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
            return redirect(f'/guru/{unique_id}/')
    else:
        raise Http404()

@login_required
def accept_request(request,unique_id,username):
    classroom = Classroom.objects.get(unique_id=unique_id)
    if member_check(request.user, classroom):
        if request.user==classroom.created_by:
            user = User.objects.get(username=username)
            classroom.members.add(user)
            classroom.pending_members.remove(user)
            return redirect(f'/guru/{unique_id}/')
    else:
        raise Http404()

@login_required
def delete_request(request,unique_id,username):
    classroom = Classroom.objects.get(unique_id=unique_id)
    if member_check(request.user, classroom):
        if request.user==classroom.created_by:
            user = User.objects.get(username=username)
            classroom.pending_members.remove(user)
            return redirect(f'/guru/{unique_id}/')
    else:
        raise Http404()