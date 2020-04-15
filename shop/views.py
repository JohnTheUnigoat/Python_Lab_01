from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import MyRegisterForm
from .forms import MyLoginForm
from django.contrib.auth.models import User
from .models import Product
from .models import ProductEntry
from .models import Cart


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


def registerView(request):
    if request.method == 'POST':
        form = MyRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
    else:
        form = MyRegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def addToCartView(request, product_id):
    user = request.user
    if user.is_authenticated:
        try:
            product_id = int(product_id)
        except ValueError:
            return redirect('main')

        product = Product.objects.filter(id=product_id).first()

        if product is None:
            return redirect('main')

        cart = user.cart;

        productEntry = cart.productEntries.filter(product=product).first()

        if productEntry is not None:
            productEntry.quantity += 1
            productEntry.save()
        else:
            productEntry = ProductEntry(product=product, quantity=1)
            productEntry.save()
            user.cart.productEntries.add(productEntry)
            user.save()

    return redirect('main')


def cartView(request):
    productEntries = request.user.cart.productEntries.all()
    username = request.user.username
    subtotal = sum(x.product.price * x.quantity for x in productEntries)

    return render(
        request, 'cart.html',
        {'entries': productEntries, 'username': username, 'subtotal': subtotal}
    )


def removeProductEntryView(request, entry_id):
    user = request.user

    if not user.is_authenticated:
        return redirect('main')

    try:
        entry = ProductEntry.objects.filter(id=entry_id).first()
    except ValueError:
        return redirect('cart')

    if entry is not None:
        entry.delete()

    return redirect('cart')


def increaseProductEntryQuantity(request, entry_id):
    return changeProductEntryQuantity(request, entry_id)

def decreaseProductEntryQuantity(request, entry_id):
    return changeProductEntryQuantity(request, entry_id, True)

def changeProductEntryQuantity(request, entry_id, decrease=False):
    user = request.user

    if not user.is_authenticated:
        return redirect('main')

    try:
        entry = ProductEntry.objects.filter(id=entry_id).first()
    except ValueError:
        return redirect('cart')

    if entry is None:
        return redirect('cart')

    if decrease:
        if entry.quantity == 1:
            entry.delete()
        else:
            entry.quantity -= 1
    else:
        entry.quantity += 1
    entry.save()

    return redirect('cart')
