from django import forms
from django.contrib.auth.models import User
from .models import Classroom, Subject, Note, Announcement, Assignment, Submission
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import *

class CreateclassForm(forms.ModelForm):
	class Meta:
		model =  Classroom
		fields = ['class_name','need_permission','description','classroom_pic']

class SubjectForm(forms.ModelForm):
	class Meta:
		model = Subject
		fields = ['subject_name']

class NoteForm(forms.ModelForm):
	class Meta:
		model = Note
		fields = ['topic','file','description']

class AssignmentForm(forms.ModelForm):
	class Meta:
		model = Assignment
		fields = ['file','topic','description',]

class AnnouncementForm(forms.ModelForm):
	class Meta:
		model = Announcement
		fields = ['file','subject','description',]

class SubmitAssignmentForm(forms.ModelForm):
	class Meta:
		model= Submission
		fields = ['file']

