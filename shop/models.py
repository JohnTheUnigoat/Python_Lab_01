from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver

import os

import pdb


class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name + " - $" + str(self.price)

@receiver(pre_delete, sender=Product)
def delete_image_on_model_delete(sender, instance, **kwargs):
    image = instance.image
    if os.path.isfile(image.path):
        os.remove(image.path)

@receiver(pre_save, sender=Product)
def delete_old_image_on_update(sender, instance, update_fields, **kwargs):
    old_image = Product.objects.get(id=instance.id).image
    new_image = instance.image

    if old_image == new_image:
        return

    if os.path.isfile(old_image.path):
        os.remove(old_image.path)



class ProductEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def totalPrice(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.product) + ' (' + str(self.quantity) + ')'



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    productEntries = models.ManyToManyField(ProductEntry, blank=True)

    def __str__(self):
        return self.user.username + "'s cart"

@receiver(post_save, sender=User)
def on_user_create(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
    else:
        instance.cart.save()
