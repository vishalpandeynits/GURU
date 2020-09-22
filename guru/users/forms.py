from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Profile

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="E-mail")

	class Meta:
		model = User
		fields = ['username', 'first_name','last_name','email', 'password1', 'password2']

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)
		self.fields['password1'].help_text = "Passwords must be of minimum 8 characters"
		self.fields['email'].widget.attrs.update({'required': 'required'})
		self.fields['first_name'].widget.attrs.update({'required': 'required'})
		self.fields['last_name'].widget.attrs.update({'required': 'required'})

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

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['bio', 'profile_pic','phone_number','whatsapp_number','facebook']

	def __init__(self, *args, **kwargs):
		super(ProfileUpdateForm, self).__init__(*args, **kwargs)
		self.fields['whatsapp_number'].label = "Whatsapp No. (with country code:)"
		self.fields['phone_number'].label = "Phone No. (with country code:)"
