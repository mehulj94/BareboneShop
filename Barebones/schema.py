import graphene
from graphene_django import DjangoObjectType

from .models import Product, Cart


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class CartType(DjangoObjectType):
    class Meta:
        model = Cart


class Query(graphene.ObjectType):
    products = graphene.List(ProductType)
    cart = graphene.List(CartType)

    def resolve_products(self, info, **kwargs):
        return Product.objects.all()

    def resolve_cart(self, info, **kwargs):
        return Cart.objects.all()
