from django.template.loader import render_to_string
from django.core.mail import EmailMessage,send_mail
from django.contrib.auth.models import User

def note_email(note):
	message = render_to_string('emails/note_add_email.html', {
		'note':note,
		'subject_name':note.subject_name,
		'classroom':note.subject_name.classroom,
	})
	mail_subject = 'A new note is added.'
	to_email = note.subject_name.classroom.members.values_list('email', flat=True)
	send_mail(mail_subject, message,'vishalpandeynits@gmail.com',to_email)

def assignment_email(assignment):
	message = render_to_string('emails/assignment_add_email.html', {
		'assignment':assignment,
		'classroom':assignment.subject_name.classroom,
	})
	mail_subject = 'A new Assignment is added.'
	to_email = assignment.subject_name.classroom.members.values_list('email', flat=True)
	send_mail(mail_subject, message,'vishalpandeynits@gmail.com',to_email)

def announcement_email(announcement):
	message = render_to_string('emails/announcement_add_email.html', {
		'announcement':announcement,
		'classroom':announcement.subject_name.classroom,
	})
	mail_subject = 'A new announcement is added.'
	to_email = announcement.subject_name.classroom.members.values_list('email', flat=True)
	send_mail(mail_subject, message,'vishalpandeynits@gmail.com',to_email)

def email_marks(request,submission,assignment):
	message = render_to_string('emails/submission_mark.html', {
		'user':request.user,
		'assignment':assignment,
		'submission':submission
	})
	mail_subject = 'marks is assigned for your submission of '+ assignment.topic
	to_email = submission.submitted_by.email
	send_mail(mail_subject, message,'vishalpandeynits@gmail.com',[to_email])	

def send_reminder(request,assignment,emails):
	message = render_to_string('emails/send_reminder.html',{
			'user':request.user,
			'assignment':assignment,
		})
	mail_subject = 'reminder for your not submitted assignment '+ assignment.topic
	send_mail(mail_subject,message,'vishalpandeynits@gmail.com',emails)