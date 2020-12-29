from django import forms
import django
from django.contrib.auth.models import User
from .models import Classroom, Subject, Note, Announcement, Assignment, Submission
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import DateInput,NumberInput
class CreateclassForm(forms.ModelForm):
	class Meta:
		model =  Classroom
		fields = ['class_name','need_permission','description','classroom_pic']
	

class SubjectForm(forms.ModelForm):
	class Meta:
		model = Subject
		fields = ['subject_name']

class SubjectEditForm(forms.ModelForm):
	class Meta:
		model = Subject
		fields = ['subject_name','subject_pic','description']

class NoteForm(forms.ModelForm):
	class Meta:
		model = Note
		fields = ['topic','file','description']


class AssignmentForm(forms.ModelForm):
	class Meta:
		model = Assignment
		fields = ['topic','full_marks','submission_date','file','description']
		widgets = {
				'submission_date': DateInput(attrs={'type': 'datetime-local'}),
				'full_marks':NumberInput(attrs={'max-value': '100'})
			}

class AnnouncementForm(forms.ModelForm):
	class Meta:
		model = Announcement
		fields = ['subject','file','description']

class SubmitAssignmentForm(forms.ModelForm):
	class Meta:
		model = Submission
		fields = ['file']

