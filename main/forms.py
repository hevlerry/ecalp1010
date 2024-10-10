from django import forms
from main.models import ContactMessage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from django import forms
from django.core.exceptions import ValidationError
from .validators import StudentEmailValidator

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@student.hau.edu.ph'):
            raise forms.ValidationError('Email must end with @student.hau.edu.ph')
        return email

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'message')