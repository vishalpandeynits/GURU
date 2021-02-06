from django import forms
from .models import Poll, Choice

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Poll
		fields = ['topic','poll_details','who_can_vote','announce_at']


class PollUpdateForm(forms.ModelForm):
	class Meta:
		model = Poll
		fields = ['topic','poll_details','announce_at']

class ChoiceForm(forms.ModelForm):
	class Meta:
		model = Choice
		fields = ['choice_text']