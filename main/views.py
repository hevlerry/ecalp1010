from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import LoginForm, RegisterForm, ContactForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages import error


def home(request):
    return render(request, 'main/index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password == confirm_password:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username is already in use!')
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Email address is already in use!')
                else:
                    user = User.objects.create_user(username, email, password)
                    user.save()
                    messages.success(request, 'You have successfully registered!')
                    return redirect('login')
            else:
                messages.error(request, 'Passwords do not match!')
        else:
            messages.error(request, 'Invalid form data!')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser or user.is_staff:
                    return redirect('custom_admin:admin_dashboard')
                else:
                    return redirect('newsfeed:newsfeed')
            else:
                messages.error(request, 'Incorrect username or password')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for contacting us!')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {'form': form})
