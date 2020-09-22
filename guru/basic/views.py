from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib import messages
from django.db.models import Q
from random import choice,randint

from .forms import *
from .models import *
import string
from .email import email_marks,send_reminder
from .delete_notify import *
#--------------------------------------------helper functions-----------------------------------
def unique_id():
    characters = string.ascii_letters + string.digits
    return  "".join(choice(characters) for x in range(randint(8,12)))

def member_check(user,classroom):
    member = classroom.members.all().filter(username=user.username)
    if member:
        return True
    raise Http404()

def proper_pagination(object,index):
    start_index,end_index = 0,10
    if object.number>index:
        start_index = object.number-index
        end_index = start_index + end_index
    return (start_index,end_index)

def pagination(request,object):
        paginator = Paginator(object,6)
        page_num=1
        if request.GET.get('page'):
            page_num = request.GET.get('page')
        query = paginator.page(page_num)
        start_index,end_index = proper_pagination(query,index=4)
        page_range = list(paginator.page_range)[start_index:end_index]
        return query,page_range


#--------------------------------------------helper functions end ------------------------------
def home(request):
    if request.user.is_authenticated:
        return redirect('/homepage/')
    return render(request,'home.html')

@login_required
def join(request,key):
    classroom = Classroom.objects.get(unique_id=key)
    if classroom.need_permission==True:
        classroom.pending_members.add(request.user)
        messages.add_message(request,message.INFO,"Your request is pending, you can access when someone let's you in.")
        return('/homepage/')
    else:
        classroom.members.add(request.user)
        messages.add_message(request,message.SUCCESS,"You have joined the classroom. Happy studing!!!")
        return redirect(f'/classroom/{key}')
    

@login_required
def homepage(request):
    #joining by key
    if request.POST.get('join_key'):
        join_key = request.POST.get('join_key')
        try:
            classroom = Classroom.objects.get(unique_id=join_key)
        except Classroom.DoesNotExist:
            messages.add_message(request, messages.WARNING,"No such classroom exists.")
            return redirect(f'/homepage/')
        if classroom.members.all().filter(username=request.user.username).exists():
            messages.add_message(request, messages.INFO,"You are already a member of this class.")
            return redirect(f'/homepage/')
        checking = classroom.need_permission
        if checking:
            classroom.pending_members.add(request.user)
            messages.add_message(request, messages.SUCCESS,"Your request is sent.\
             You can acsess classroom when someone lets you in.")
            return redirect(f'/homepage/')
        else:
            classroom.members.add(request.user)
            notify = Classroom_activity(classroom=classroom,actor=request.user)
            notify.action = "A new member "+str(request.user.username)+ "Have joined your classroom."
            notify.save()
    
    #create classroom
    if request.method=='POST':
        createclassform = CreateclassForm(request.POST or None)
        if createclassform.is_valid():
            classroom=createclassform.save(commit=False)
            classroom.unique_id = unique_id()
            classroom.created_by = request.user
            classroom.save()
            classroom.teacher.add(request.user)
            classroom.members.add(request.user)
            classroom.special_permissions.add(request.user)
            return redirect(f'/guru/{classroom.unique_id}/')
    else:
        createclassform = CreateclassForm()

    #queryset
    my_classes = Classroom.objects.all().filter(members=request.user)
    params={
        'createclassform':createclassform,
        'my_classes':my_classes
        }
    return render(request,'homepage.html',params)

@login_required
def admin_status(request,unique_id,username):
    classroom = Classroom.objects.get(unique_id=unique_id)
    admin = classroom.special_permissions.filter(username=request.user.username).exists()
    if admin:
        check = classroom.special_permissions.filter(username = username).exists()
        if check:
            if classroom.created_by == User.objects.get(username=username):
                messages.add_message(request,messages.WARNING,"This user have created this class. He can't be dropped")
                return redirect(f'/classroom/{unique_id}/')
            classroom.special_permissions.remove(User.objects.get(username=username))
            return redirect(f'/classroom/{unique_id}')
        else:
            classroom.special_permissions.add(User.objects.get(username=username))
            return redirect(f'/classroom/{unique_id}')  
    else:
        raise Http404()


@login_required
def classroom_page(request,unique_id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    if member_check(request.user, classroom):
        members = classroom.members.all()
        teachers = classroom.teacher.all()
        students = members.difference(teachers)
        pending_members = classroom.pending_members.all()
        admins = classroom.special_permissions.all()
        classes = Classroom.objects.all().filter(members=request.user)
        is_admin = classroom.created_by == request.user
        #classroom_update
        if request.method=="POST":
            form = CreateclassForm(request.POST,request.FILES,instance=classroom)
            if form.is_valid():
                form.save()
                return redirect(f'/classroom/{unique_id}/')
        else:
            form = CreateclassForm(instance=classroom)
        params={
            'students':students,
            'teachers':teachers,
            'pending_members':pending_members,
            'classroom':classroom,
            'is_admin':is_admin,
            'form':form,
            'admins':admins,
            'classes':classes
        }
        return render(request,'classroom.html',params)

@login_required
def subjects(request, unique_id, form = None):
    classroom = Classroom.objects.get(unique_id=unique_id)
    if member_check(request.user,classroom):
        #querysets
        members = classroom.members.all()
        subjects = Subject.objects.all().filter(classroom=classroom)
        subject_teacher_check = Classroom.objects.filter(teacher=request.user).exists()
        admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
        classes = Classroom.objects.all().filter(members=request.user)
        is_teacher = subject_teacher_check or admin_check

        # Admins can add a subject with its teacher
        if admin_check:
            if request.method=="POST": 
                form = SubjectForm(request.POST)
                if form.is_valid():
                    subject=form.save(commit=False)
                    subject.classroom=classroom
                    try:
                        teacher = User.objects.get(username=request.POST.get('teacher'))
                        if not teacher and not members.filter(username=teacher.username).exists():
                            messages.add_message(request,messages.WARNING,"This user is not a member of this class. Tell him to join this classroom first.")
                        else:
                            subject.teacher = teacher
                            subject.save()
                            subject.upload_permission.add(teacher)
                            messages.add_message(request,messages.INFO,"Subject added")
                            classroom.teacher.add(teacher)
                            return redirect(f'/guru/{unique_id}/')
                            
                    except User.DoesNotExist:
                        messages.add_message(request,messages.WARNING,"No such User exists.")
            else:
                form = SubjectForm()
        params = {
            'subjects':subjects,
            'form':form,
            'classroom':classroom,
            'is_teacher':is_teacher,
            'classes':classes
            }
        return render(request,'subjects.html',params)

@login_required
def subject_page(request,unique_id,subject_id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    if member_check(request.user,classroom):
        subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
        params = {
            'subject':subject,
            'classroom':classroom,
        }   
        return render(request,'subject_page.html',params)

@login_required
def resource(request,unique_id,subject_id,form = None):
    classroom = Classroom.objects.get(unique_id=unique_id)
    if member_check(request.user,classroom):

        #querysets
        subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
        notes = Note.objects.all().filter(subject_name=subject).order_by('-id')
        if request.GET.get('search'):
            search = request.GET.get('search')
            notes = notes.filter(Q(topic__icontains=search)|Q(description__icontains=search)) 

        query,page_range = pagination(request, notes)
        upload_permission = subject.upload_permission.all().filter(username=request.user.username).exists()
        admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
        is_teacher = admin_check or upload_permission or request.user==subject.teacher  

        #Add note form handling
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

        params={
            'form':form,
            'subject':subject,
            'classroom':classroom,
            'notes':notes,
            'page':query,
            'page_range':page_range,
            'is_teacher':is_teacher,
            }
        return render(request,'resources/resources.html',params)

@login_required
def read_note(request, unique_id, subject_id, id, form = None):
    classroom = Classroom.objects.get(unique_id=unique_id)
    if member_check(request.user,classroom):
        #queryset
        subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
        notes = Note.objects.all().filter(subject_name=subject)
        note = Note.objects.get(id=id)
        upload_permission = subject.upload_permission.filter(username=request.user.username).exists()
        admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
        is_teacher = admin_check or upload_permission or request.user==subject.teacher 

        #Note update form handling
        if is_teacher:
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
                'is_teacher': is_teacher,
            }
        return render(request,'resources/read_note.html',params)

@login_required
def resource_delete(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.get(id=subject_id)
    note = Note.objects.get(id=id)
    upload_permission = subject.upload_permission.filter(username=request.user.username).exists()
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    is_teacher = admin_check or upload_permission or request.user==subject.teacher 
    if is_teacher:
        note.delete()
        note_delete_notify(request,note)
        return redirect(f'/{unique_id}/{subject_id}/resource/')
    else:
        raise Http404()

@login_required
def assignment(request ,unique_id, subject_id, form=None):
    classroom = Classroom.objects.get(unique_id=unique_id)
    if member_check(request.user,classroom):
        subject = Subject.objects.get(id=subject_id)
        admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
        is_teacher = admin_check or subject.teacher==request.user

        #add assignent form handling
        if is_teacher:
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

        #queryset
        assignments = Assignment.objects.all().filter(subject_name=subject).order_by('-id')
        search = request.GET.get('search')
        if search:
            assignments = assignments.filter(Q(topic__icontains=search)|Q(description__icontains=search))
        query,page_range = pagination(request,assignments)
        assignments=query.object_list

        params={
            'form':form,
            'subject':subject,
            'classroom':classroom,
            'assignments':assignments,
            'page':query,
            'page_range':page_range,
            }
        return render(request,'assignments/assignments.html',params)

@login_required
def assignment_page(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    if member_check(request.user, classroom):

        #querysets
        updateform = form = submitted = not_submitted = submission = None
        subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
        assignments = Assignment.objects.all().filter(subject_name=subject).order_by('submission_date').reverse()
        assignment = Assignment.objects.all().filter(subject_name=subject).get(id=id)

        #list of submissions
        try:
            submission = Submission.objects.all().filter(assignment=assignment,submitted_by=request.user)
        except Submission.DoesNotExist:
            pass

        all_submissions = Submission.objects.all().filter(assignment=assignment)
        late_submissions = Submission.objects.all().filter(submitted_on__gt=assignment.submission_date)
        ontime_submissions = all_submissions.difference(late_submissions)
        admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
        is_teacher = admin_check or request.user==subject.teacher

        #update assignment
        if is_teacher:
            if request.method=="POST":
                updateform = AssignmentForm(request.POST,request.FILES,instance=assignment)
                if updateform.is_valid():
                    assignmentform = updateform.save(commit=False)
                    assignmentform.subject_name = subject
                    assignmentform.save()
                    return redirect(f'/{unique_id}/{subject_id}/{assignment.id}/assignment/')
            else:
                updateform= AssignmentForm(instance=assignment)

            # assigning marks by techer for each assignment
            if request.POST.get('marks_assigned'):
                id  = request.POST.get('id')
                submission = Submission.objects.get(id=id)
                marks = request.POST.get('marks_assigned')
                submission.marks_assigned = marks
                submission.save()
                email_marks(request,submission,assignment)

                return redirect(f'/{unique_id}/{subject_id}/{assignment.id}/assignment/')
        submission_object = None
        #submitting assignment
        if not is_teacher:
            submission_object = Submission.objects.filter(Q(submitted_by=request.user) & Q(assignment=assignment)).first()
            if request.method=="POST":
                form = SubmitAssignmentForm(request.POST, request.FILES,instance=submission_object)
                if form.is_valid():
                    data=form.save(commit=False)
                    data.submitted_by=request.user
                    data.assignment= assignment
                    data.current_status = True
                    data.save()
                    assignment.submitted_by.add(request.user)
                    return redirect(f'/{unique_id}/{subject_id}/{assignment.id}/assignment/')
            else:
                form = SubmitAssignmentForm(instance=submission_object)

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
            'submission_object':submission_object
            }
        #list of submitted and not_submitted_students
        if is_teacher:          
            members = classroom.members.all()
            teachers = classroom.teacher.all()
            students = members.difference(teachers)
            submitted = assignment.submitted_by.all()
            not_submitted = students.difference(submitted)
            params['submitted']=submitted
            params['not_submitted']=not_submitted
            if request.POST.get('send_reminder')=='1':
                send_reminder(request,assignment,not_submitted.values_list('email', flat=True))
        return render(request,'assignments/assignment_page.html',params)

@login_required
def assignment_delete(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    assignment = Assignment.objects.all().filter(subject_name=subject).get(id=id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    is_teacher = admin_check or request.user==subject.teacher
    if is_teacher:
        assignment.delete()
        assignment_delete_notify(request,assignment)
        return redirect(f'/{unique_id}/{subject_id}/assignments/')
    else:
        raise Http404()

@login_required
def announcement(request, unique_id, subject_id):
    form = None
    classroom = Classroom.objects.get(unique_id=unique_id)
    if member_check(request.user, classroom):

        #querysets
        subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
        admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
        is_teacher = admin_check or request.user==subject.teacher
        announcements = Announcement.objects.all().filter(subject_name=subject).order_by('-id')
        if request.GET.get('search'):
            search = request.GET.get('search')
            announcements = announcements.filter(Q(subject__icontains=search)|Q(description__icontains=search))
        query,page_range = pagination(request,announcements)
        announcements=query.object_list

        #announcement form handling
        if is_teacher:
            if request.method=="POST":
                form = AnnouncementForm(request.POST,request.FILES)
                if form.is_valid():
                    announcement = form.save(commit=False)
                    announcement.subject_name = subject
                    announcement.announced_by = request.user
                    announcement.save()
            else:
                form= AnnouncementForm()

        params={
                'form':form,
                'subject':subject,
                'classroom':classroom,
                'announcements':announcements,
                'page':query,
                'page_range':page_range,
                'is_teacher':is_teacher
            }
        return render(request,'announcements/announcement.html',params)

@login_required
def announcement_page(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    form = None
    if member_check(request.user, classroom):

        #queryset
        subject = Subject.objects.get(id=subject_id)
        announcements = Announcement.objects.all().filter(subject_name=subject).order_by('issued_on','-id')
        announcement = Announcement.objects.get(id=id)
        admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
        is_teacher = admin_check or request.user==subject.teacher

        #announcement update handling
        if is_teacher:
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
            'is_teacher':is_teacher,
            }
        return render(request,'announcements/announcement_page.html',params)

@login_required
def announcement_delete(request,unique_id,subject_id,id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    announcement = Announcement.objects.all().filter(subject_name=subject).get(id=id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    is_teacher = admin_check or request.user==subject.teacher
    if is_teacher:
        announcement.delete()
        announcement_delete_notify(request,announcement)
        return redirect(f'/{unique_id}/{subject_id}/announcement/')
    else:
        raise Http404()

@login_required
def this_subject(request,unique_id, subject_id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    if member_check(request.user, classroom):
        subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
        admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
        upload_permission = subject.upload_permission.all()
        members = classroom.members.all()
        admins = classroom.special_permissions.all()
        teachers = classroom.teacher.all()
        subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
        teacher = subject.teacher
        members = admins.distinct() | members.difference(teachers).distinct()
        activities = Subject_activity.objects.filter(subject=subject).order_by('-id')
        query,page_range = pagination(request,activities)
        activities=query.object_list
        if request.method=='POST':
            form = SubjectEditForm(request.POST , request.FILES,instance=subject)
            if form.is_valid():
                form.save()
        else:
            form = SubjectEditForm(instance=subject)
        params={
            'subject':subject,
            'classroom':classroom, 
            'is_teacher':admin_check,
            'members':members,
            'upload_permissions':upload_permission,
            'admins':admins,
            'teacher':teacher,
            'page':query,
            'page_range':page_range,
            'form':form
                    }
        return render(request,'thissubject.html',params)

@login_required
def delete_subject(request,unique_id, subject_id):
    classroom = Classroom.objects.get(unique_id=unique_id)
    subject = Subject.objects.all().filter(classroom=classroom).get(id=subject_id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()

    if admin_check:
        subject.delete()
        notify = Classroom_activity(classroom=classroom,actor=request.user)
        notify.action = "A Subject "+subject.subject_name + " is deleted by "+request.user.username
        notify.save()
        return redirect(f'/guru/{unique_id}/')
    else:
        raise Http404()

@login_required
def remove_member(request,unique_id,username):
    classroom = Classroom.objects.get(unique_id=unique_id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    if admin_check or request.user==User.objects.get(username=username):
        classroom.members.remove(User.objects.get(username=username))
        if request.user==User.objects.get(username=username):
            return redirect('/homepage/')  
        else:
            return redirect(f'/classroom/{unique_id}/')
    else:
        raise Http404()

@login_required
def accept_request(request,unique_id,username):
    classroom = Classroom.objects.get(unique_id=unique_id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()

    if admin_check:
        user = User.objects.get(username=username)
        classroom.members.add(user)
        classroom.pending_members.remove(user)
        notify = Classroom_activity(classroom=classroom,actor=request.user)
        notify.action = "A new member "+ str(user.username) + "have joined your classroom."
        notify.save()
        return redirect(f'/classroom/{unique_id}/')

@login_required
def delete_request(request,unique_id,username):
    classroom = Classroom.objects.get(unique_id=unique_id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    if request.user==classroom.created_by:
        user = User.objects.get(username=username)
        classroom.pending_members.remove(user)
        return redirect(f'/classroom/{unique_id}/')

@login_required
def manage_upload_permission(request,unique_id,subject_id,username):
    classroom = Classroom.objects.get(unique_id=unique_id)  
    if member_check(request.user,classroom):
        user = User.objects.get(username=username)
        subject = Subject.objects.get(id=subject_id)
        check = subject.upload_permission.filter(username = user.username).exists()
        if check:
            subject.upload_permission.remove(user)
            return redirect(f'/{unique_id}/{subject_id}/this_subject')
        else:
            subject.upload_permission.add(user)
            return redirect(f'/{unique_id}/{subject_id}/this_subject')

