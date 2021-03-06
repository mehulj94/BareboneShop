from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=200,blank=False)
    price = models.IntegerField(default=0)
    inventory_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Cart(models.Model):
    owner = models.ForeignKey('auth.User', related_name='products', on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    product_cnt = models.IntegerField(default=0)
    checked_out = models.BooleanField(default=False)

    def __str__(self):
        return self.product