from django import forms
from .models import Poll, Choice

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Poll
		fields = ['file','topic','poll_details','who_can_vote']

	def __init__(self, *args, **kwargs):
		super(QuestionForm, self).__init__(*args, **kwargs)
		self.fields['poll_details'].widget.attrs.update({'id': 'textarea'})


class ChoiceForm(forms.ModelForm):
	class Meta:
		model = Choice
		fields = ['choice_text']