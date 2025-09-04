from django.db import models
from django.contrib.auth.models import User


class Products(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'products'

class Orders(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, db_column='productid')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, db_column='customerid')
    quantity = models.IntegerField(default=1)
    order_time = models.DateTimeField(auto_now_add=True, null = True)

    def __str__(self):
        return f"{self.customer.username} - {self.product.name} x {self.quantity}"
    
    class Meta:
        db_table = 'orders'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'cart'
        unique_together = ('user', 'product')