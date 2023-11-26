from django import forms
from .models import Chat


class ChatForm(forms.ModelForm):

	class Meta:
		model = Chat
		fields = ('name', 'avatar', 'type_chat', 'members')

	def clean(self):
		data = self.cleaned_data
		return data
