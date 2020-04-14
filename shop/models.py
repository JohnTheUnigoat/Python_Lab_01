from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import pdb

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name + " - $" + str(self.price)

# TODO: impement file deletion on model delete

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.user.username + "'s cart"

@receiver(post_save, sender=User)
def on_user_create(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
    else:
        instance.cart.save()
