from django.shortcuts import render
from .models import Product

def index(request):
    context = {
        'products': Product.objects.all(),
        'username': request.user.username
    }
    return render(request, 'index.html', context)
