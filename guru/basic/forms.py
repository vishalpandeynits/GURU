from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Classroom, Subject, Note, Announcement, Assignment

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    class Meta:
        model = User
        fields = ("username",'first_name','last_name',"email",'password1','password2',)

class CreateclassForm(forms.ModelForm):
	class Meta:
		model =  Classroom
		fields = ['class_name']

class SubjectForm(forms.ModelForm):
	class Meta:
		model = Subject
		fields = ['subject_name','subject_teacher']

class NoteForm(forms.ModelForm):
	class Meta:
		 model = Note
		 fields = ['subject_name','topic','file','description']

class AssignmentForm(forms.ModelForm):
	class Meta:
		model = Assignment
		fields = ['file','topic','description','submission_date']

class AnnouncementForm(forms.ModelForm):
	class Meta:
		model = Announcement
		fields = ['file','subject','description',]