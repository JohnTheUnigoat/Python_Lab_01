"""Lab_01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from shop import views as shopviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', shopviews.loginView, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', shopviews.registerView, name='register'),
    path('', shopviews.index, name='main'),
    path('addtocart/<product_id>/', shopviews.addToCartView),
    path('cart/', shopviews.cartView, name='cart'),
    path('cart/removeProductEntry/<entry_id>/', shopviews.removeProductEntryView),
    path('cart/incEntryQuantity/<entry_id>/', shopviews.increaseProductEntryQuantity),
    path('cart/decEntryQuantity/<entry_id>/', shopviews.decreaseProductEntryQuantity),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
