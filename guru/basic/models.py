from django.db import models
from django.contrib.auth.models import User
import random
import string
from django.contrib.auth.models import AbstractUser

def unique_id():
    chars= string.ascii_letters + string.digits
    result_str = ''.join((random.choice(chars) for i in range(8)))
    return result_str

class Classroom(models.Model):
	created_by = models.ForeignKey(User, on_delete = models.CASCADE,related_name='create_by')
	class_name = models.CharField(max_length = 100)
	created_on = models.DateTimeField(auto_now_add=True)
	unique_id = models.CharField(max_length=10,unique=True,default=unique_id(), editable=False)
	members = models.ManyToManyField(User)
	teacher = models.ManyToManyField(User,related_name='teacher')

	def __str__(self):
		return self.class_name

class Subject(models.Model):
	classroom = models.ForeignKey(Classroom, on_delete = models.CASCADE)
	subject_name = models.CharField(max_length=50)
	subject_teacher = models.CharField(max_length=50)

	def __str__(self):
		return self.subject_name

class Note(models.Model):
	subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE)
	uploaded_on = models.DateTimeField(auto_now_add= True)
	file = models.FileField(upload_to='media/notes/',null=True,blank=True)
	topic = models.CharField(max_length=100,)
	description = models.TextField(max_length=500,)

	def __str__(self):
		return self.topic

class Announcement(models.Model):
	subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE)
	issued_on = models.DateTimeField(auto_now_add= True)
	subject = models.CharField(max_length=100)
	description = models.TextField(max_length=500,)
	file = models.FileField(upload_to='media/announcement/',)
	
	def __str__(self):
		return self.subject

class Assignment(models.Model):
	subject_name = models.ForeignKey(Subject,on_delete=models.CASCADE)
	uploaded_on = models.DateTimeField(auto_now_add= True)
	file = models.FileField(upload_to='media/',null=True,blank = True)
	topic = models.CharField(max_length=100,)
	description = models.TextField(max_length=500,)
	submission_date = models.DateTimeField() 

	def __str__(self):
		return "Assignment on "+ self.topic

class Submission(models.Model):
	assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
	file = models.FileField(upload_to="Submissions/",null=True,blank=True)
	submitted_by = models.ForeignKey(User,on_delete=models.CASCADE)
	submitted_on = models.DateTimeField(auto_now_add=True)

	def __self__(self):
		return self.submitted_by

class Poll(models.Model):
	file = models.FileField(upload_to="poll/",null=True,blank=True)
	topic = models.CharField(max_length=100,null=True,blank = True)
	description = models.TextField(max_length=100)
	declare_result_at = models.DateTimeField()
	voter = models.ForeignKey(User,on_delete = models.DO_NOTHING)

