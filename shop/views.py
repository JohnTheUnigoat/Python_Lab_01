from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import MyUserCreationForm
from .forms import MyLoginForm
from django.contrib.auth.models import User
from .models import Product

import pdb

def index(request):
    context = {
        'products': Product.objects.all(),
        'username': request.user.username
    }
    return render(request, 'index.html', context)


def loginView(request):
    if request.method == 'POST':
        form = MyLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main')
    else:
        form = MyLoginForm()

    return render(request, 'registration/login.html', {'form': form})


def register(request):
    # if request.user.is_authenticated:
    #     return redirect('main')

    # if request.method == 'POST':
    #     form = MyUserCreationForm(data=request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         login(request, user)
    #         return redirect('main')
    # else:
    # TODO: custom registration form
    form = MyUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
