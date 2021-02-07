from django import forms
from .models import Classroom, Subject, Note, Announcement, Assignment, Submission
from django.forms.widgets import NumberInput

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

