from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_delete
from django.dispatch import receiver
from .email import *

class Classroom(models.Model):
	created_by = models.ForeignKey(User, on_delete = models.CASCADE,related_name='created_by')
	members = models.ManyToManyField(User)
	teacher = models.ManyToManyField(User, related_name='classroom_teachers')
	special_permissions = models.ManyToManyField(User, related_name= "special_permissions")
	pending_members = models.ManyToManyField(User,related_name='pending_members')
	classroom_pic = models.ImageField(default="classroom.jpg",upload_to="classrooms/",null=True)
	class_name = models.CharField(max_length = 100)
	description = models.TextField(null=True, blank=True)
	created_on = models.DateTimeField(auto_now_add=True)
	unique_id = models.CharField(max_length=16,unique=True)
	need_permission = models.BooleanField(default=True)

	def __str__(self):
		return self.class_name

class Subject(models.Model):
	classroom = models.ForeignKey(Classroom, on_delete = models.CASCADE)
	subject_name = models.CharField(max_length=50)
	teacher = models.ForeignKey(User,on_delete=models.CASCADE,related_name="teacher")
	upload_permission = models.ManyToManyField(User,related_name="upload_permitted")
	subject_pic = models.ImageField(upload_to="subject_content/")
	description = models.TextField(max_length=500)

	def __str__(self):
		return self.subject_name

class Note(models.Model):
	subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE)
	uploaded_on = models.DateTimeField(auto_now_add= True)
	file = models.FileField(upload_to='media/notes/',null=True,blank=True,)
	topic = models.CharField(max_length=100,)
	description = models.TextField()
	uploaded_by = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.topic

class Announcement(models.Model):
	subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE)
	issued_on = models.DateTimeField(auto_now_add= True)
	subject = models.CharField(max_length=100)
	description = models.TextField()
	file = models.FileField(upload_to='media/announcement/',null=True,)
	announced_by = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.subject

class Assignment(models.Model):
	subject_name = models.ForeignKey(Subject,on_delete=models.CASCADE)
	uploaded_on = models.DateTimeField(auto_now_add= True)
	file = models.FileField(upload_to='media/',null=True,blank = True)
	topic = models.CharField(max_length=100)
	description = models.TextField()
	submission_date = models.DateTimeField() 
	assigned_by = models.ForeignKey(User,on_delete=models.CASCADE)
	submitted_by = models.ManyToManyField(User,related_name="Submissions")
	full_marks = models.IntegerField(default=100)
	
	def __str__(self):
		return "Assignment on "+ self.topic

class Submission(models.Model):
	assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
	file = models.FileField(upload_to="Submissions/")
	submitted_by = models.ForeignKey(User,on_delete=models.CASCADE)
	submitted_on = models.DateTimeField(auto_now_add=True)
	current_status = models.BooleanField(default=False)
	marks_assigned = models.IntegerField(null=True,blank=True)

	def __str__(self):
		return "Assignment upload of "+self.assignment.topic + self.submitted_by.username

class Subject_activity(models.Model):
	subject = models.ForeignKey(Subject, on_delete = models.CASCADE)
	action = models.CharField(max_length=100)
	actor = models.ForeignKey(User,on_delete = models.DO_NOTHING)
	time = models.DateTimeField(auto_now_add = True)
	url = models.URLField(null=True,blank=True)

	def __str__(self):
		return self.action

class Classroom_activity(models.Model):
	classroom = models.ForeignKey(Classroom, on_delete = models.CASCADE)
	action = models.CharField(max_length=100)
	actor = models.ForeignKey(User,on_delete = models.DO_NOTHING)
	time = models.DateTimeField(auto_now_add = True)
	url = models.URLField(null=True,blank=True)

	def __str__(self):
		return self.action


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

@receiver(post_save, sender=Note)
def note_tracker(sender, instance, created, **kwargs):
	if created:
		activity = Subject_activity(subject=instance.subject_name,actor=instance.uploaded_by)
		activity.action = "A new note is added."
		activity.save()

@receiver(post_save, sender=Announcement)
def announcement_tracker(sender, instance, created,**kwargs):
	if created:
		activity = Subject_activity(subject=instance.subject_name,actor=instance.announced_by)
		activity.action = "A new Announcement is added."
		activity.save()

@receiver(post_save, sender=Assignment)
def assignment_tracker(sender, instance, created, **kwargs):
	if created:
		activity = Subject_activity(subject=instance.subject_name,actor=instance.assigned_by)
		activity.action = f"A new Assignment is added. Submission date is {instance.submission_date}"
		activity.save()

@receiver(post_save,sender=Subject)
def classroom_tracker(sender, instance, created, **kwargs):
	if created:
		activity = Classroom_activity(classroom=instance.classroom,actor=instance.classroom.created_by)#CHECK
		activity.action = f"A new subject is added."
		activity.save()