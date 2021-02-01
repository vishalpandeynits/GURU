from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Profile
import django

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="E-mail")

	class Meta:
		model = User
		fields = ['username', 'first_name','last_name','email', 'password1', 'password2']

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)
		self.fields['password1'].help_text = None
		self.fields['username'].help_text = None
		self.fields['password2'].help_text = None
		self.fields['password2'].label = 'Confirm Password'
		self.fields['email'].widget.attrs.update({'required': 'required'})
		self.fields['first_name'].widget.attrs.update({'required': 'required'})
		self.fields['last_name'].widget.attrs.update({'required': 'required'})

	def clean(self):
		cleaned_data = self.cleaned_data
		cleaned_data['username']=cleaned_data['username'].lower()
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
		    if len(cleaned_data['username'])>16 or len(cleaned_data['username'])<4:
		    	raise ValidationError('username must be between 8 to 16 characters long.')

		except User.DoesNotExist:
		    pass
		else:
		    raise forms.ValidationError('User already exists! Try different one!')
		return cleaned_data


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Username/Email:'
			

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['bio', 'profile_pic','phone_number','whatsapp_number']

	def __init__(self, *args, **kwargs):
		super(ProfileUpdateForm, self).__init__(*args, **kwargs)
		self.fields['whatsapp_number'].label = "Whatsapp No. (with country code:)"
		self.fields['phone_number'].label = "Phone No. (with country code:)"
