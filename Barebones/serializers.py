from django.contrib.auth.models import User
from rest_framework import serializers
from Barebones.models import Product, Cart


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
