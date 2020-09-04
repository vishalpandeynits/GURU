from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .email import *

class Classroom(models.Model):
	created_by = models.ForeignKey(User, on_delete = models.CASCADE,related_name='created_by')
	class_name = models.CharField(max_length = 100)
	created_on = models.DateTimeField(auto_now_add=True)
	unique_id = models.CharField(max_length=16,unique=True)
	members = models.ManyToManyField(User)
	teacher = models.ManyToManyField(User,related_name='teacher')
	pending_members = models.ManyToManyField(User,related_name='pending_members')

	def __str__(self):
		return self.class_name

class Subject(models.Model):
	classroom = models.ForeignKey(Classroom, on_delete = models.CASCADE)
	subject_name = models.CharField(max_length=50)
	teacher = models.ForeignKey(User,on_delete=models.CASCADE)
	
	def __str__(self):
		return self.subject_name

class Note(models.Model):
	subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE)
	uploaded_on = models.DateTimeField(auto_now_add= True)
	file = models.FileField(upload_to='media/notes/',null=True,blank=True)
	topic = models.CharField(max_length=100,)
	description = models.TextField(max_length=500,)
	uploaded_by = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.topic

class Announcement(models.Model):
	subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE)
	issued_on = models.DateTimeField(auto_now_add= True)
	subject = models.CharField(max_length=100)
	description = models.TextField(max_length=500,)
	file = models.FileField(upload_to='media/announcement/',)
	announced_by = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.subject

class Assignment(models.Model):
	subject_name = models.ForeignKey(Subject,on_delete=models.CASCADE)
	uploaded_on = models.DateTimeField(auto_now_add= True)
	file = models.FileField(upload_to='media/',null=True,blank = True)
	topic = models.CharField(max_length=100,)
	description = models.TextField(max_length=500,)
	submission_date = models.DateTimeField() 
	assigned_by = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return "Assignment on "+ self.topic

class Submission(models.Model):
	assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
	file = models.FileField(upload_to="Submissions/",null=True,blank=True)
	submitted_by = models.ForeignKey(User,on_delete=models.CASCADE)
	submitted_on = models.DateTimeField(auto_now_add=True)

	def __self__(self):
		return self.submitted_by

@receiver(post_save, sender=Note)
def note_signal(sender, instance, created, **kwargs):
	if created:
		note_email(instance)

@receiver(post_save, sender=Announcement)
def announcement_signal(sender, instance, created, **kwargs):
	if created:
		announcement_email(instance)

@receiver(post_save, sender=Assignment)
def assignment_signal(sender, instance, created, **kwargs):
	if created:
		assignment_email(instance)


