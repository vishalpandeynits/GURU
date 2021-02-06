from django.db import models
from django.contrib.auth.models import User
from .email import *
from django_quill.fields import QuillField
from imagekit.models import ProcessedImageField
from guru.storage_back import PrivateMediaStorage
from imagekit.processors import ResizeToFill

class Classroom(models.Model):
	created_by = models.ForeignKey(User, on_delete = models.CASCADE,related_name='created_by')
	members = models.ManyToManyField(User)
	teacher = models.ManyToManyField(User, related_name='classroom_teachers')
	special_permissions = models.ManyToManyField(User, related_name= "special_permissions")
	pending_members = models.ManyToManyField(User,related_name='pending_members')
	classroom_pic = ProcessedImageField(upload_to="classroom",default="classroom.jpg",storage=PrivateMediaStorage(),null=True,
	processors=[ResizeToFill(1000, 1000)],format='JPEG',options={'quality': 100})
	class_name = models.CharField(max_length = 50)
	description = models.TextField(null=True, blank=True,max_length=300)
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
	subject_pic = ProcessedImageField(upload_to="subject_content",default="book.jpg",storage=PrivateMediaStorage(),
	processors=[ResizeToFill(1000, 1000)],format='JPEG',options={'quality': 100})
	description = models.TextField(null=True,blank=True,max_length=500)

	def __str__(self):
		return self.subject_name

class Note(models.Model):
	subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE)
	uploaded_on = models.DateTimeField(auto_now_add= True)
	file = models.FileField(storage=PrivateMediaStorage(),upload_to="notes",null=True,blank=True,)
	topic = models.CharField(max_length=100,)
	description = QuillField()
	uploaded_by = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.topic

class Announcement(models.Model):
	subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE)
	issued_on = models.DateTimeField(auto_now_add= True)
	subject = models.CharField(max_length=100)
	description = QuillField()
	file = models.FileField(storage=PrivateMediaStorage(),upload_to="announcements",null=True,blank=True)
	announced_by = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.subject

class Assignment(models.Model):
	subject_name = models.ForeignKey(Subject,on_delete=models.CASCADE)
	uploaded_on = models.DateTimeField(auto_now_add= True)
	file = models.FileField(storage=PrivateMediaStorage(),upload_to="assignments",null=True,blank = True,)
	topic = models.CharField(max_length=100,)
	description = QuillField()
	submission_date = models.DateTimeField() 
	assigned_by = models.ForeignKey(User,on_delete=models.CASCADE)
	submitted_by = models.ManyToManyField(User,related_name="Submissions")
	full_marks = models.IntegerField(default=100)
	submission_link = models.BooleanField(default=True)

	def __str__(self):
		return "Assignment on "+ self.topic

class Submission(models.Model):
	assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
	file = models.FileField(storage=PrivateMediaStorage(),upload_to="submissions",)
	submitted_by = models.ForeignKey(User,on_delete=models.CASCADE)
	submitted_on = models.DateTimeField(auto_now_add=True)
	current_status = models.BooleanField(default=False)
	marks_assigned = models.IntegerField(null=True,blank=True)
	history = models.CharField(max_length=5000,null=True,blank=True)
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