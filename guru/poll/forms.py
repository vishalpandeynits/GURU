from django import forms
from .models import Poll, Choice

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Poll
		fields = ['file','poll_details','who_can_vote']


class ChoiceForm(forms.ModelForm):
	class Meta:
		model = Choice
		fields = ['choice_text']