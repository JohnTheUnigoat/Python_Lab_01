from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name + " - $" + str(self.price)

# TODO: impement file deletion on model delete
