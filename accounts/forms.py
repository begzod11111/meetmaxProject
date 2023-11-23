from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

from accounts.models import Profile


class RegistrationUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {

            "username": forms.TextInput(attrs={
                'placeholder': "Username",
                'class': 'form__input',
                'id': "username"
            }),

            "email": forms.EmailInput(attrs={
                "placeholder": "Email",
                'class': 'form__input'
            }),
            'password1': forms.PasswordInput(attrs={
                "placeholder": "Password",
            }),
            'password2': forms.PasswordInput(attrs={
                "placeholder": "Reset password",
            })

        }

    def clean_email(self):
        data = self.cleaned_data.get('email')
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data


class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'birthday', 'instagram', 'twitter', 'website', 'facebook', 'avatar')
        widgets = {
            'avatar': forms.FileInput(attrs={
            }),
            'birthday': forms.DateInput(),
        }

    def clean_bio(self):
        bio = self.cleaned_data['bio']
        if bio.isdigit():
            self.add_error('bio', ValidationError(
                'Bio cannot contain only numbers',
                code='invalid'))
        return bio


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email')

    def clean(self):
        data = self.cleaned_data
        qs = User.objects.exclude(id=self.instance.id).filter(email=data['email'])
        us = User.objects.exclude(id=self.instance.id).filter(username=data['username'])

        if qs.exists():
            self.add_error('email', ValidationError(
                'Email already in use.',
                code='invalid'))
        if data['last_name'].isdigit():
            self.add_error('last_name', ValidationError(
                "Last name cannot contain only numbers",
                code="invalid"))
        if data['first_name'].isdigit():
            self.add_error('first_name', ValidationError(
                "First name cannot contain only numbers",
                code="invalid"))
        if us.exists() or data['username'].isdigit():
            self.add_error('username', ValidationError(
                "This name is already in use or cannot contain only numbers",
                code="invalid"))
        return data


