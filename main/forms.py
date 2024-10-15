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

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['confirm_password'].widget.attrs.update({'class': 'form-control'})

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search("[a-z]", password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search("[A-Z]", password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search("[^A-Za-z0-9]", password):
            raise ValidationError("Password must contain at least one special character.")
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@student.hau.edu.ph'):
            raise forms.ValidationError('Email must end with @student.hau.edu.ph')
        return email

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'message')