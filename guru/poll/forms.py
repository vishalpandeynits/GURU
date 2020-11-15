from django import forms
from .models import Poll, Choice
from django.forms.widgets import DateInput

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Poll
		fields = ['topic','poll_details','who_can_vote']


class PollUpdateForm(forms.ModelForm):
	class Meta:
		model = Poll
		fields = ['topic','poll_details','announce_at']
		widgets = {
				'announce_at': DateInput(attrs={'type': 'datetime-local'}),
			}

class ChoiceForm(forms.ModelForm):
	class Meta:
		model = Choice
		fields = ['choice_text']