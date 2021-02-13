from .models import *
from notifications.signals import notify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

@receiver(post_save, sender=Note)
def note_signal(sender, instance, created, **kwargs):
	if created:
		students = instance.subject_name.classroom.members.all().difference(instance.subject_name.classroom.teacher.all()).difference(instance.subject_name.classroom.special_permissions.all())
		activity = Subject_activity(subject=instance.subject_name,actor=instance.uploaded_by)
		activity.action = "A new note is added."
		activity.url = reverse('read_note', kwargs={
			'unique_id':instance.subject_name.classroom.unique_id,
			'subject_id':instance.subject_name.id,
			'id':instance.id
			})
		activity.save()
		notify.send(sender=instance.uploaded_by,recipient=students,verb=activity.action,url= activity.url)
		note_email(instance)

@receiver(post_save, sender=Announcement)
def announcement_signal(sender, instance, created, **kwargs):
	if created:
		activity = Subject_activity(subject=instance.subject_name,actor=instance.announced_by)
		activity.action = "A new Announcement is added."
		activity.url = reverse('announcement_page',kwargs={
		'unique_id':instance.subject_name.classroom.unique_id,
		'subject_id':instance.subject_name.id,
		'id':instance.id
		})
		activity.save()
		recepients = instance.subject_name.classroom.members.all().exclude(username=instance.announced_by.username)
		notify.send(sender=instance.announced_by,recipient=recepients,verb=activity.action,url= activity.url)
		announcement_email(instance)

@receiver(post_save, sender=Assignment)
def assignment_signal(sender, instance, created, **kwargs):
	if created:
		activity = Subject_activity(subject=instance.subject_name,actor=instance.assigned_by)
		activity.action = f"A new Assignment is added. Submission date is {instance.submission_date}"
		activity.url = reverse('assignment_page',kwargs={
		'unique_id':instance.subject_name.classroom.unique_id,
		'subject_id':instance.subject_name.id,
		'id':instance.id
		})
		activity.save()
		students = instance.subject_name.classroom.members.all().difference(instance.subject_name.classroom.teacher.all()).difference(instance.subject_name.classroom.special_permissions.all())
		notify.send(sender=instance.assigned_by,recipient=students,verb=activity.action,url= activity.url)
		assignment_email(instance)