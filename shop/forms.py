from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

import pdb

class MyLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        min_length=4, max_length=100
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        res = User.objects.filter(username=username)
        if len(res) == 0:
            raise ValidationError("This user isn't registered!")
        return username

    def clean(self):
        if 'username' in self.errors:
            return

        username = self.cleaned_data.get('username')
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError('Wrong password!')


class MyRegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        min_length=4, max_length=100
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        res = User.objects.filter(username=username)
        if len(res) > 0:
            raise ValidationError("Username already taken!")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if 'username' in self.errors:
            return password2

        validate_password(password1)

        if password1 != password2:
            raise ValidationError("Passwords don't match!")

        return password2

    def save(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password2']
        user = User.objects.create_user(username=username, password=password)
        return user