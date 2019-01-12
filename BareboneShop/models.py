from django.db import models


class Product(models.Model):
    product_id = models.IntegerField(default=0, primary_key=True)
    title = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    inventory_cnt = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Cart(models.Model):
    cart_id = models.CharField(max_length=200, primary_key=True)
    product_id = models.IntegerField(default=0)
    product = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    product_cnt = models.IntegerField(default=0)
    checked_out = models.BooleanField(default=False)

    def __str__(self):
        return self.cart_id
