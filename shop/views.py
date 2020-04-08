from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product

def index(request):
    context = {
        'products': Product.objects.all(),
        'username': request.user.username
    }
    return render(request, 'index.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
