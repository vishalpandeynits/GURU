from django import forms
from django.contrib.auth.models import User
from django.forms import ClearableFileInput
from .models import Classroom, Subject, Note, Announcement, Assignment, Submission
from bootstrap_datepicker_plus import DateTimePickerInput
from .fields import MultiFileField, MultiMediaField, MultiImageField

class CreateclassForm(forms.ModelForm):
	class Meta:
		model =  Classroom
		fields = ['class_name']

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
		fields = ['file','topic','description','submission_date']
		widgets = {
  				'submission_date': DateTimePickerInput(),
  				}

class AnnouncementForm(forms.ModelForm):
	class Meta:
		model = Announcement
		fields = ['file','subject','description',]
		widgets = {
  				
				}

class SubmitAssignmentForm(forms.ModelForm):
	class Meta:
		model= Submission
		fields = ['file']
		widgets = {
  				}