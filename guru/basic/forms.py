from django import forms
from django.contrib.auth.models import User
from django.forms import ClearableFileInput
from .models import Classroom, Subject, Note, Announcement, Assignment, Submission
from bootstrap_datepicker_plus import DateTimePickerInput
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

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
		fields = ['file','topic','description']

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
class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="E-mail")

	class Meta:
		model = User
		fields = ['username', 'first_name','last_name','email', 'password1', 'password2']


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)
		self.fields['password1'].help_text = "Passwords must be of minimum 8 characters"
		self.fields['username'].label = "Username:"
		self.fields['email'].widget.attrs.update({'required': 'required'})

	def clean(self):
		cleaned_data = self.cleaned_data

		# checking Email unique

		try:
		    User.objects.get(email=cleaned_data['email'])
		except User.DoesNotExist:
		    pass
		else:
		    raise ValidationError('This Email address already exists! Try different one!')

		# checking User unique

		try:
		    User.objects.get(username=cleaned_data['username'])
		except User.DoesNotExist:
		    pass
		else:
		    raise forms.ValidationError('User already exists! Try different one!')

		return cleaned_data
