from django.db import models

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.BooleanField(default=True)
    image = models.ImageField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)  # Add the quantity field

    def __str__(self):
        return self.name
