import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from .models import Product, Cart


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class CartProduct(graphene.ObjectType):
    product = graphene.String()
    product_cnt = graphene.Int()
    total_cost = graphene.Int()


class CartType(graphene.ObjectType):
    products = graphene.List(CartProduct)
    cart_amount = graphene.Int()


class Query(graphene.ObjectType):
    products = graphene.List(ProductType, id=graphene.Int(), avl=graphene.Int())
    cart = graphene.List(CartType)

    def resolve_products(self, info, search=None, **kwargs):
        id = kwargs.get('id')
        inv_cnt = kwargs.get('avl')

        if id is not None:
            return Product.objects.filter(id=id)

        if inv_cnt == 1:
            return Product.objects.filter(inventory_count__gt=0)

        return Product.objects.all()


    def resolve_cart(self, info, **kwargs):
        cart_items = Cart.objects.all()
        prods = []
        out_prod = []
        tot = 0

        for item in cart_items:
            dictionary = CartProduct(item.product, item.product_cnt,(item.product_cnt * item.price))
            prods.append(dictionary)
            tot = tot + (item.product_cnt * item.price)

        c = CartType(prods,tot)
        out_prod.append(c)
        return out_prod


class CreateProduct(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()
    price = graphene.Int()
    inventory_count= graphene.Int()

    #2
    class Arguments:
        title = graphene.String()
        price = graphene.Int()
        inventory_count = graphene.Int()

    #3
    def mutate(self, info, title, price, inventory_count):
        prod = Product(title=title, price=price, inventory_count=inventory_count)
        prod.save()

        return CreateProduct(
            id=prod.id,
            title=prod.title,
            price=prod.price,
            inventory_count=prod.inventory_count,
        )


class CreatePurchaseProduct(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String()
    price = graphene.Int()
    inventory_count= graphene.Int()
    status = graphene.String()

    class Arguments:
        title = graphene.String()
        price = graphene.Int()
        inventory_count = graphene.Int()
        status = graphene.String()

    def mutate(self, info, title, price, inventory_count):
        try:
            prod = Product.objects.get(title=title)
        except Product.DoesNotExist:
            raise GraphQLError('Product does not exist')

        # Validations
        if prod.price != price:
            raise GraphQLError('Invalid product price')

        if inventory_count <= 0:
            raise GraphQLError('Invalid inventory count')

        if prod.inventory_count >= inventory_count:
            # Updating inventory count
            prod.inventory_count -= inventory_count
        elif prod.inventory_count == 0:
            raise GraphQLError('Product unavailable')
        else:
            raise GraphQLError('Insufficient product inventory')

        status = "Product purchased successfully"
        prod.save()

        return CreatePurchaseProduct(
            title=title,
            price=price,
            inventory_count=inventory_count,
            status=status,
        )


class CreateAddCart(graphene.Mutation):
    id = graphene.Int()
    product = graphene.String()
    price = graphene.Int()
    product_cnt= graphene.Int()
    checked_out = graphene.Boolean()
    status = graphene.String()

    #2
    class Arguments:
        product = graphene.String()
        price = graphene.Int()
        product_cnt = graphene.Int()
        checked_out = graphene.Boolean()
        status = graphene.String()

    #3
    def mutate(self, info, product, price, product_cnt):
        flag = 0
        cart = Cart()
        prod = Product()

        # Get product details from the database
        try:
            prod = Product.objects.get(title=product)
        except Product.DoesNotExist:
            raise GraphQLError('Product does not exist')

        # Get data from cart
        try:
            cart = Cart.objects.get(product=product)
        except Cart.DoesNotExist:
            flag = 1 # set flag if item is added to cart for the first time
            cart = Cart(owner=info.context.user,product=product,price=price,product_cnt=product_cnt, checked_out=False)

        # Validations
        if prod.price != price:
            raise GraphQLError('Invalid product price')

        if product_cnt <= 0:
            raise GraphQLError('Invalid inventory count')

        if prod.inventory_count < product_cnt:
            raise GraphQLError('Insufficient product inventory')

        # Updating cart
        if flag == 0:
            cart.product_cnt += product_cnt
        elif flag == 1:
            cart.product_cnt = product_cnt

        checked_out = False
        status = "Product added to cart successfully"
        cart.save()

        return CreateAddCart(
            product=product,
            price=price,
            product_cnt=product_cnt,
            checked_out=checked_out,
            status=status,
        )


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    create_purchaseproduct = CreatePurchaseProduct.Field()
    create_addcart = CreateAddCart.Field()

