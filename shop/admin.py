from django.contrib import admin
from .models import Product
from .models import ProductEntry
from .models import Cart
from .models import Order

admin.site.register(Product)
admin.site.register(ProductEntry)
admin.site.register(Cart)
admin.site.register(Order)
