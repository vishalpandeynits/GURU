from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.http import Http404,HttpResponse
from django.contrib import messages
from django.db.models import Q
from .forms import *
from .models import *
from .email import *
from .delete_notify import *
from .utils import *
from django.urls import reverse
import xlwt,datetime 
from notifications.signals import notify
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt #checked
def home(request): 
    """Landing Page"""
    if request.user.is_authenticated:
        return redirect(reverse('homepage'))
    else:
        if request.method=='POST':
            name=request.POST.get('name')
            email = request.POST.get('email')
            message =f"{name} \n {email} \n {request.POST.get('message')} "
            mail_subject = 'Contact us : Sent by ' + name 
            if(send_mail(mail_subject,message,'guru.online.classroom.portal@gmail.com',['guru.online.classroom.portal@gmail.com'])):
                messages.add_message(request,messages.SUCCESS,'Your message sent successfully.')
            else:
                messages.add_message(request,messages.ERROR,"An Error while sending your message.\
                    Please try again or contact using given contact details.")
    return render(request,'intro.html')
    
@login_required#checked
def homepage(request):
    """
    Create a classroom, Join A classroom, 
    """
    user = request.user
    if request.POST.get('join_key'):
        join_key = request.POST.get('join_key')
        try:
            classroom = Classroom.objects.get(unique_id=join_key)
        except Classroom.DoesNotExist:
            messages.add_message(request, messages.WARNING,"No such classroom exists.")
            return redirect(reverse('homepage'))
        if classroom.members.all().filter(username=user.username).exists():
            messages.add_message(request, messages.INFO,"You are already member of this class.")
            return redirect(reverse('homepage'))

        if classroom.need_permission:
            classroom.pending_members.add(user)
            messages.add_message(request, messages.SUCCESS,"Your request is sent.\
             You can access classroom material when someone lets you in.")
            user.profile.pending_invitations.add(classroom)
            notify.send(sender=user,verb=f"{user.username} wants to join {classroom.class_name}",recipient=classroom.special_permissions.all(),
            url=reverse('classroom_page',kwargs={
                'unique_id':classroom.unique_id
            }
            ))
        else:
            recipients = User.objects.filter(username__in=classroom.members.values_list('username', flat=True))
            url = reverse('profile',kwargs={'username':user.username})
            notify.send(sender=user,recipient=recipients,verb=f"{request.user.username} has joined {classroom.class_name}",url= url)
            classroom.members.add(user)
        return redirect(reverse('homepage'))

    #create classroom
    if request.method=='POST':
        createclassform = CreateclassForm(request.POST ,request.FILES)
        if createclassform.is_valid():
            classroom=createclassform.save(commit=False)
            classroom.unique_id = unique_id()
            classroom.created_by = request.user
            classroom.save()
            classroom.members.add(request.user)
            classroom.special_permissions.add(request.user)
            return redirect(reverse('homepage'))
    else:
        createclassform = CreateclassForm()

    #queryset
    params={
        'createclassform':createclassform,
        }
    return render(request,'homepage.html',params)

@login_required#checked
def admin_status(request,unique_id,username):
    """
    Toggles admin status of users from a classroom
    """
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    admin = classroom.special_permissions.filter(username=request.user.username).exists()
    if admin:
        check = classroom.special_permissions.filter(username = username).exists()
        user = User.objects.get(username=username)
        url = reverse('classroom_page',kwargs={ 'unique_id':unique_id})
        if check:
            if classroom.created_by == user:
                messages.add_message(request,messages.WARNING,"This user have created\
                 this class. He can't be dropped")
                return redirect(reverse('classroom_page',kwargs={'unique_id':classroom.unique_id}))
            classroom.special_permissions.remove(user)
            notify.send(sender=request.user,recipient = user,verb=f"You are no longer admin of {classroom.class_name}",url=url)
        else:
            classroom.special_permissions.add(user)
            notify.send(sender=request.user,recipient = user,verb=f"Now you are admin of {classroom.class_name}",url=url)

        return redirect(reverse('classroom_page',kwargs={'unique_id':classroom.unique_id})) 
    else:
        raise Http404()

@login_required#checked
def classroom_page(request,unique_id):
    """
    Classroom Setting Page.
    """
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    if member_check(request.user, classroom):
        pending_members = classroom.pending_members.all()
        admins = classroom.special_permissions.all()
        members =  admins | classroom.members.all()
        is_admin = classroom.special_permissions.filter(username = request.user.username).exists()
        #classroom_update
        if request.method=="POST":
            form = CreateclassForm(request.POST,request.FILES,instance=classroom)
            if form.is_valid():
                form.save()
                return redirect(reverse('subjects',kwargs={'unique_id':classroom.unique_id}))
        else:
            form = CreateclassForm(instance=classroom)
        params={
            'members':members.distinct(),
            'admins':admins,
            'pending_members':pending_members,
            'classroom':classroom,
            'is_admin':is_admin,
            'form':form,
        }
        return render(request,'classroom_settings.html',params)

@login_required#checked
def subjects(request, unique_id,form=None):
    """ 
    Enlists all the subjects of a classroom ,
    subjects can be added by admins
    """
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    if member_check(request.user,classroom):
        #querysets
        members = classroom.members.all()
        subjects = Subject.objects.filter(classroom=classroom)
        admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
        # Admins can add a subject and assign a teacher to it
        if admin_check and request.method=="POST":
            form = SubjectForm(request.POST)
            teacher = User.objects.get(username=request.POST.get('teacher'))
            if form.is_valid():
                subject=form.save(commit=False)
                subject.classroom=classroom
                subject.teacher = teacher
                subject.save()
                subject.upload_permission.add(teacher)
                recipients=User.objects.filter(username__in=classroom.members.values_list('username', flat=True))
                url = reverse('subjects',kwargs={'unique_id':classroom.unique_id})
                notify.send(sender=request.user,verb=f"subject {subject.subject_name} added in {classroom.class_name}",
                recipient=recipients,url=url)
                messages.add_message(request,messages.INFO,f"A new Subject {subject.subject_name} added")
                classroom.teacher.add(teacher)
                return redirect(url)
            else:
                form = SubjectForm()
        params = {
            'subjects':subjects,
            'form':form,
            'classroom':classroom,
            'is_admin':admin_check,
            'members':members
            }
        return render(request,'subjects_list.html',params)

@login_required#checked
def notes_list(request,unique_id,subject_id,form = None):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    if member_check(request.user,classroom):
        #querysets
        subject = Subject.objects.get(id=subject_id)
        notes = Note.objects.filter(subject_name=subject).order_by('-id')
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
                if form.is_valid:
                    data=form.save(commit=False)
                    data.subject_name = subject
                    data.uploaded_by = request.user
                    data.save()
                    messages.add_message(request,messages.SUCCESS,f"Your Note {data.topic} is added")
                    return redirect(reverse('resources',kwargs={'unique_id':classroom.unique_id,'subject_id':subject.id}))
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
        return render(request,'notes/notes_list.html',params)

@login_required#checked
def note_details(request, unique_id, subject_id, id, form = None):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    if member_check(request.user,classroom):
        #queryset
        subject = Subject.objects.get(id=subject_id) 
        note = Note.objects.get(id=id)
        admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
        is_teacher = admin_check or request.user==subject.teacher or note.uploaded_by == request.user

        if is_teacher:
            if request.method=="POST": 
                form = NoteForm(request.POST,request.FILES,instance=note)
                if form.is_valid():
                    form.file = request.POST.get('file')
                    form.save()
                    return redirect(reverse('read_note',kwargs={
                        'unique_id':classroom.unique_id,
                        'subject_id':subject.id,
                        'id':note.id
                        }))
            else:
                form= NoteForm(instance=note)
        params={
                'subject':subject,
                'updateform':form,
                'note':note,
                'classroom':classroom,
                'is_teacher': is_teacher,
                'extension':extension_type(note.file)
            }
        return render(request,'notes/note_detail.html',params)

@login_required#checked
def note_delete(request,unique_id,subject_id,id):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    subject = get_object_or_404(Subject,id=subject_id)
    note =  get_object_or_404(Note,id=subject_id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    is_teacher = admin_check or note.uploaded_by==request.user or request.user==subject.teacher 
    if is_teacher:
        note.delete()
        note_delete_notify(request,note)
        return redirect(reverse('resources',kwargs={'unique_id':classroom.unique_id,'subject_id':subject.id}))
    else:
        raise Http404()

@login_required#checked
def assignments_list(request ,unique_id, subject_id, form=None):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    if member_check(request.user,classroom):
        subject = Subject.objects.get(id=subject_id)
        assignments = Assignment.objects.filter(subject_name=subject).reverse()
        search = request.GET.get('search')
        if search:
            assignments = assignments.filter(Q(topic__icontains=search)|Q(description__icontains=search))
        query,page_range = pagination(request,assignments)
        assignments=query.object_list

        admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
        is_teacher = admin_check or subject.teacher==request.user

        if is_teacher:
            if request.method=="POST":
                form = AssignmentForm(request.POST,request.FILES)
                if form.is_valid():
                    assignment = form.save(commit=False)
                    assignment.subject_name = subject
                    assignment.assigned_by = request.user
                    assignment.save()
                    return redirect(reverse('assignments',kwargs=
                        {'unique_id':classroom.unique_id,'subject_id':subject.id,}))
            else:
                form= AssignmentForm()

        params={
            'form':form,
            'subject':subject,
            'classroom':classroom,
            'assignments':assignments,
            'page':query,
            'page_range':page_range,
            }
        return render(request,'assignments/assignment_list.html',params)

@login_required#checked
def assignment_details(request,unique_id,subject_id,id):
    updateform = form  = submission = submission_object = None
    classroom = Classroom.objects.get(unique_id=unique_id)
    if member_check(request.user, classroom):
        subject = Subject.objects.get(id=subject_id)
        assignment = Assignment.objects.get(id=id)
        admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
        is_teacher = admin_check or request.user==subject.teacher
        if is_teacher:
            if request.method=="POST":
                updateform = AssignmentForm(request.POST,request.FILES,instance=assignment)
                if updateform.is_valid():
                    updateform.save()
                    return redirect(reverse('assignment_page',kwargs={
                        'unique_id':classroom.unique_id,'subject_id':subject.id,'id':assignment.id}))
            else:
                updateform= AssignmentForm(instance=assignment)
        #submitting assignment
        else: 
            submission_object = Submission.objects.filter(Q(submitted_by=request.user) & Q(assignment=assignment)).first()
            if request.method=="POST":
                if assignment.submission_link:
                    form = SubmitAssignmentForm(request.POST, request.FILES,instance=submission_object)
                    if form.is_valid():
                        data=form.save(commit=False)
                        data.submitted_by=request.user
                        data.assignment= assignment
                        data.save()
                        assignment.submitted_by.add(request.user)
                        return redirect(reverse('assignment_page',kwargs=
                            {'unique_id':classroom.unique_id,'subject_id':subject.id,'id':assignment.id}))
                else:
                    messages.add_message(request,messages.WARNING,"Submission link is closed.")
            else:
                form = SubmitAssignmentForm(instance=submission_object)
        
        params={
            'assignment':assignment,
            'extension':extension_type(assignment.file),
            'subject':subject,
            'form':form,
            'updateform':updateform,
            'classroom':classroom,
            'submissionform':form,
            'submission':submission,
            'submission_object':submission_object,
            'is_teacher':is_teacher,
            }       
        return render(request,'assignments/assignment_detail.html',params)

@login_required#checked
def assignment_handle(request,unique_id,subject_id,id):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    is_admin = classroom.special_permissions.filter(username = request.user.username).exists()
    subject = get_object_or_404(Subject,id=subject_id)
    is_teacher = request.user==subject.teacher
    if is_admin or is_teacher:
        assignment = Assignment.objects.get(id=id)
        if request.POST.get('marks_assigned'):
            id  = request.POST.get('id') 
            submission = Submission.objects.get(id=id)
            marks = request.POST.get('marks_assigned')
            submission.marks_assigned = marks
            submission.save()
            url = reverse('assignment_page',kwargs={'unique_id':classroom.unique_id,'subject_id':subject.id,'id':assignment.id})
            notify.send(sender=request.user,verb=f'You got {marks} for your assignment {assignment.topic}',recipient=submission.submitted_by,url =url)
            email_marks(request,submission,assignment)
            return redirect(reverse('assignment-handle',kwargs={
                'unique_id':classroom.unique_id,
                'subject_id':subject.id,
                'id':assignment.id
                }))

        #list of submissions
        all_submissions = Submission.objects.filter(assignment=assignment)
        late_submissions = all_submissions.filter(submitted_on__gt=assignment.submission_date)
        ontime_submissions = all_submissions.filter(submitted_on__lte=assignment.submission_date)
        members = classroom.members.all()
        teachers = classroom.teacher.all()
        students = members.difference(teachers)
        submitted = assignment.submitted_by.all()
        not_submitted = students.difference(submitted)
        
        if request.POST.get('send_reminder')=='1':
            recepients = User.objects.filter(username__in=not_submitted.values_list('username', flat=True))
            url = reverse('assignment_page',kwargs={'unique_id':classroom.unique_id,'subject_id':subject.id,'id':assignment.id})
            notify.send(sender=request.user,verb=f"Reminder to submit your assignment",recipient=recepients,url=url)
            send_reminder(request,assignment,not_submitted.values_list('email', flat=True))

        if request.POST.get('toggle_link'):
            if assignment.submission_link:
                assignment.submission_link  = False
            else:
                assignment.submission_link = True 
            assignment.save()
        params = {
            'assignment':assignment,
            'all_submissions':all_submissions,
            'late_submissions':late_submissions,
            'ontime_submissions':ontime_submissions,
            'is_teacher':is_teacher,
            'submitted':submitted,
            'not_submitted':not_submitted,
            'subject':subject,
            'classroom':classroom,
        }
        return render(request,'assignments/assignment_handle.html',params)
    else:
        raise Http404()

@login_required#checked
def assignment_delete(request,unique_id,subject_id,id):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    subject = get_object_or_404(Subject,id=subject_id)
    assignment = get_object_or_404(Assignment,id=id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    is_teacher = admin_check or request.user==subject.teacher
    if is_teacher:
        assignment.delete()
        assignment_delete_notify(request,assignment)
        return redirect(reverse('assignment_page',kwargs={'unique_id':classroom.unique_id,'subject_id':subject.id}))
    else:
        raise Http404()

@login_required#checked
def announcements_list(request, unique_id, subject_id,form = None):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    if member_check(request.user, classroom):
        #querysets
        subject = get_object_or_404(Subject,id=subject_id)
        admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
        is_teacher = admin_check or request.user==subject.teacher
        announcements = Announcement.objects.all().filter(subject_name=subject).reverse()
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
                    return redirect(reverse('announcement',kwargs=
                        {'unique_id':classroom.unique_id,'subject_id':subject.id}))
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
        return render(request,'announcements/announcement_list.html',params)

@login_required#checked
def announcement_details(request,unique_id,subject_id,id,form = None):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    if member_check(request.user, classroom):
        subject = get_object_or_404(Subject,id=subject_id)
        announcement = get_object_or_404(Announcement,id=id)
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
                    return redirect(reverse('announcement_page',kwargs={
                        'unique_id':classroom.unique_id,
                        'subject_id':subject.id,
                        'id':announcement.id
                        }))
            else:
                form= AnnouncementForm(instance=announcement)
        params={
            'announcement':announcement,
            'extension':extension_type(announcement.file),
            'subject':subject,
            'updateform':form,
            'classroom':classroom,
            'is_teacher':is_teacher,
            }
        return render(request,'announcements/announcement_details.html',params)

@login_required #checked
def announcement_delete(request,unique_id,subject_id,id):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    subject = get_object_or_404(Subject,id=subject_id)
    announcement = get_object_or_404(Announcement,id=id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    is_teacher = admin_check or request.user==subject.teacher
    #notify
    if is_teacher:
        announcement.delete()
        announcement_delete_notify(request,announcement)
        return redirect(reverse('announcement',kwargs={
            'unique_id':classroom.unique_id,
            'subject_id':subject.id
            }))
    else:
        raise Http404()

@login_required #checked
def subject_details(request,unique_id, subject_id):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    if member_check(request.user, classroom):
        subject = get_object_or_404(Subject,id=subject_id)
        admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
        upload_permission = subject.upload_permission.all()
        members = classroom.members.all()
        admins = classroom.special_permissions.all()
        teachers = classroom.teacher.all()
        teacher = subject.teacher
        members = list((admins| members.difference(teachers)).distinct())
        if teacher not in members:
            members.append(teacher)

        activities = Subject_activity.objects.filter(subject=subject).reverse()
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
        return render(request,'subject_details.html',params)

@login_required #checked
def delete_subject(request,unique_id, subject_id):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    subject = get_object_or_404(Subject,id=subject_id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    if admin_check:
        verb = "A Subject "+subject.subject_name + " is deleted by "+ request.user.username
        url =reverse('subjects',kwargs={'unique_id':classroom.unique_id})
        recipient = User.objects.filter(username__in=classroom.members.values_list('username', flat=True))
        notify.send(sender=request.user,verb=verb,recipient=recipient,url=url)
        subject.delete()
        return redirect(url)
    else:
        raise Http404()

@login_required #checked
def remove_member(request,unique_id,username):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    remove_this_user = get_object_or_404(User,username=username)
    url = reverse('classroom_page',kwargs={'unique_id':classroom.unique_id})
    if admin_check or request.user==remove_this_user:
        if remove_this_user == classroom.created_by:
            messages.add_message(request,messages.WARNING,"This user can't be dropped. He has created this classroom.")
            return redirect(url)
        classroom.members.remove(remove_this_user)
        classroom.teacher.remove(remove_this_user)
        classroom.special_permissions.remove(remove_this_user)
        verb = f"You are removed from {classroom.class_name}"
        notify.send(sender=request.user,verb=verb,recipient=remove_this_user,url='#')
        if request.user==remove_this_user:
            return redirect(reverse('homepage'))
        else:
            return redirect(url)
    else:
        raise Http404()

@login_required #checked
def accept_request(request,unique_id,username):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    if admin_check:
        user = get_object_or_404(User,username=username)
        classroom.members.add(user)
        classroom.pending_members.remove(user)
        user.profile.pending_invitations.remove(classroom)
        url = reverse('subjects',kwargs={'unique_id':classroom.unique_id})
        verb = f'Yor request to join classroom {classroom.class_name} is accepted'
        notify.send(sender=request.user,verb=verb,recipient=user,url=url)
        return redirect(reverse('classroom_page',kwargs={'unique_id':classroom.unique_id}))

@login_required#checked
def delete_request(request,unique_id,username):
    """ If you don't want to accept the request """
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    if admin_check:
        user = User.objects.get(username=username)
        classroom.pending_members.remove(user)
        verb = "Your request to join class {classroom.class_name} is rejected"
        url = "#"
        notify.send(sender=request.user,verb=verb,recipient=user,url=url)
        return redirect(reverse('classroom_page',kwargs={'unique_id':classroom.unique_id}))

@login_required #checked
def manage_upload_permission(request,unique_id,subject_id,username):
    classroom = Classroom.objects.get(unique_id=unique_id)  
    if member_check(request.user,classroom):
        user = User.objects.get(username=username)
        subject = Subject.objects.get(id=subject_id)
        check = subject.upload_permission.filter(username = user.username).exists()
        url = reverse('subjects',kwargs={'unique_id':classroom.unique_id})
        if check:
            verb = f"You can't upload notes in {subject.subject_name} of {classroom.class_name} anymore"
            notify.send(sender=request.user,verb=verb,recipient=user,url = url)
            subject.upload_permission.remove(user)
        else:
            verb = f"You got permission to  upload notes in {subject.subject_name} of {classroom.class_name}"
            subject.upload_permission.add(user)
            notify.send(sender=request.user,verb=verb,recipient=user,url = url)
        return redirect(reverse('subject_details',kwargs={'unique_id':classroom.unique_id,'subject_id':subject.id}))

@login_required#checked
def unsend_request(request,unique_id):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    if classroom in request.user.profile.pending_invitations.all():
        request.user.profile.pending_invitations.remove(classroom)
        classroom.pending_members.remove(request.user)
        return redirect(reverse('profile',kwargs={
            'username':request.user.username
        }))
    else:
        raise Http404()

@login_required#checked
def export_marks(request,unique_id,subject_id,id):
    classroom = get_object_or_404(Classroom,unique_id=unique_id)
    admin_check = classroom.special_permissions.filter(username = request.user.username).exists()
    subject = get_object_or_404(Subject,id=subject_id)
    if admin_check or request.user==subject.teacher:
        assignment = get_object_or_404(Assignment,id=id)
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="mark_sheet of {assignment.topic}.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Submissions')
        # Sheet header, first row
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Username','submitted_on','marks_obtained']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        
        rows = Submission.objects.all().filter(assignment=assignment).values_list('submitted_by','submitted_on','marks_assigned')
        rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]
        
        for row in rows:
            row_num += 1
            row[0]=str(User.objects.get(id=row[0]))
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        wb.save(response)
        return response
    else:
        raise Http404()

def features(request):
    return render(request, 'features.html')

def privacy(request):
    return render(request, 'privacy.html')