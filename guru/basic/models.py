from django.db import models
from django.contrib.auth.models import User
import uuid

class Classroom(models.Model):
	# created_by = models.ForeignKey(User,on_delete = models.CASCADE)
	class_name = models.CharField(max_length = 100)
	created_on = models.DateTimeField(auto_now_add=True)
	unique_id = models.CharField(max_length=10,unique=True,default=str(uuid.uuid4())[0:8], editable=False)
	members = models.ManyToManyField(User)
	teacher = models.ForeignKey(User, on_delete = models.CASCADE,related_name='teacher')

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
	file = models.FileField(upload_to='media/')
	topic = models.CharField(max_length=100,null=True,blank=True)
	description = models.CharField(max_length=500, null= True,blank = True)

	def __str__(self):
		return self.topic

class Announcement(models.Model):
	subject_name = models.ForeignKey(Subject, on_delete=models.CASCADE)
	issued_on = models.DateTimeField(auto_now_add= True)
	subject = models.CharField(max_length=100)
	description = models.CharField(max_length=500, null= True,blank = True)
	file = models.FileField(upload_to='media/',null=True,blank = True)
	
	def __str__(self):
		return self.subject

class Assignment(models.Model):
	subject_name = models.ForeignKey(Subject,on_delete=models.CASCADE)
	uploaded_on = models.DateTimeField(auto_now_add= True)
	file = models.FileField(upload_to='media/',null=True,blank = True)
	topic = models.CharField(max_length=100,null=True,blank=True)
	description = models.CharField(max_length=500, null= True,blank = True)
	submission_date = models.DateTimeField()

	def __str__(self):
		return "Assignment on"+ self.topic