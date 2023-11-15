from django import forms

from post.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('descriptions', 'media', 'file', 'author')
        widgets = {
            'media': forms.FileInput(attrs={
                'type': 'file'
            }),
            'file': forms.FileInput(attrs={
                'type': 'file'
            }),
            'author': forms.TextInput(attrs={
            }),
        }
