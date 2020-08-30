from django import forms
from .models import *

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Poll
		fields = ['file','poll_details']

class ChoiceForm(forms.ModelForm):
	class Meta:
		model = Choice
		fields = ['choice_text']