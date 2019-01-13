from Barebones.models import Product, Cart
from Barebones.serializers import ProductSerializer, CheckoutSerializer
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import Http404
from rest_framework import permissions
from Barebones.permission import IsOwnerOrReadOnly


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'products': reverse('product-list', request=request, format=format),
        'Cart': reverse('cart-list', request=request, format=format)
    })


class ProductList(generics.ListCreateAPIView):
    """
    Retrieve all products, or create a new product.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveAPIView):
    """
    Retrieve a single product.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductAvlList(generics.ListAPIView):
    """
    List all available products.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Product.objects.filter(inventory_count__gt=0)
    serializer_class = ProductSerializer


class ProductPurchase(APIView):
    """
    Purchase a product. Inventory count is reduced.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        product = self.get_object(pk)
        if product.inventory_count > 0:
            data = {"inventory_count": product.inventory_count - 1}
        else:
            raise Http404
        serializer = ProductSerializer(product, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCart(APIView):
    """
    Add a product to Cart.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def get_object(self, pk):
        try:
            return Cart.objects.get(product=pk)
        except Product.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):

        product = Product.objects.get(id=pk)

        product_name = request.data.get('product')
        product_price = request.data.get('price')
        product_count = request.data.get('product_cnt')
        checked_out = request.data.get('checked_out')
        owner = request.data.get('owner')
        try:
            shop = Cart.objects.get(product=product.title)
            flag = 1
        except:
            flag = 0

        #Below code verifies the incoming data
        #If the incoming data does not match the data in database
        #then error is thrown
        if product.inventory_count < 1:
            raise Http404
        elif product.title != product_name:
            return Response({"Error": "Invalid Product Name"}, status=status.HTTP_400_BAD_REQUEST)
        elif product.price != product_price:
            return Response({"Error": "Invalid Product Price"}, status=status.HTTP_400_BAD_REQUEST)
        elif product_count > product.inventory_count:
            return Response({"Error": "Insufficient Inventory"}, status=status.HTTP_400_BAD_REQUEST)
        elif checked_out == True:
            return Response({"Error": "Cannot checkout. Set to False for adding to cart"},
                            status=status.HTTP_400_BAD_REQUEST)
        elif owner != request.data.get('owner'):
            return Response({"Error": "Incorrect Owner"}, status=status.HTTP_400_BAD_REQUEST)
        elif flag == 1:

            data = {"product_cnt": shop.product_cnt + product_count}
            serializer = CheckoutSerializer(shop, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"success": True}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewCart(APIView):
    """
    View Cart
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def get(self, request, format=None):
        queryset = Cart.objects.all()
        products_included = {}
        total_amount = 0

        for item in queryset:
            total_amount = total_amount + (item.product_cnt * item.price)
            products_included[item.product] = item.product_cnt

        return Response({"Products": products_included, "Total Amount": total_amount}, status=status.HTTP_200_OK)


class CheckoutCart(APIView):
    """
    Checkout Cart
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def post(self, request, format=None):
        cart_items = Cart.objects.all()

        for items in cart_items:
            products = Product.objects.get(title=items.product)
            products.inventory_count = products.inventory_count - items.product_cnt
            products.save()
            items.delete()

        return Response({"Success": "Cart Checkout Successful"}, status=status.HTTP_200_OK)
