from django.template.loader import render_to_string
from django.core.mail import EmailMessage,send_mail
from django.contrib.auth.models import User

def note_email(note):
	message = render_to_string('note_add_email.html', {
		'note':note,
		'subject_name':note.subject_name,
		'classroom':note.subject_name.classroom,
	})
	mail_subject = 'A new note is added.'
	to_email = note.subject_name.classroom.members.values_list('email', flat=True)
	send_mail(mail_subject, message,'vishalpandeynits@gmail.com',to_email)

def assignment_email(assignment):
	message = render_to_string('assignment_add_email.html', {
		'assignment':assignment,
		'classroom':assignment.subject_name.classroom,
	})
	mail_subject = 'A new Assignment is added.'
	to_email = assignment.subject_name.classroom.members.values_list('email', flat=True)
	send_mail(mail_subject, message,'vishalpandeynits@gmail.com',to_email)

def announcement_email(announcement):
	message = render_to_string('announcement_add_email.html', {
		'announcement':announcement,
		'classroom':announcement.subject_name.classroom,
	})
	mail_subject = 'A new announcement is added.'
	to_email = announcement.subject_name.classroom.members.values_list('email', flat=True)
	send_mail(mail_subject, message,'vishalpandeynits@gmail.com',to_email)

