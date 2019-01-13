from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import json
from .models import Product, Cart


class ProductCartCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        client = APIClient()
        normal_user = User.objects.create_user(username="joe", password="password", email="joe@example.com")
        self.client.login(username='joe', password='password')

    def test_api_can_create_a_product(self):
        """Test the api has product creation capability."""

        product_data_1 = {"title": "Iphone 7", "price": "800", "inventory_count": "25"}
        product_data_2 = {"title": "Iphone 8", "price": "1000", "inventory_count": "15"}

        response1 = self.client.post(reverse('product-list'), product_data_1, format='json')
        response2 = self.client.post(reverse('product-list'), product_data_2, format='json')

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.get(title='Iphone 7').title, 'Iphone 7')

    def test_api_can_get_all_product(self):
        """Test the api can get all products."""
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_get_single_product(self):
        """Test the api can get a single product."""
        self.test_api_can_create_a_product()
        response = self.client.get('/products/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Iphone 7')

    def test_api_can_get_all_avl_product(self):
        """Test the api can get all available products."""
        self.test_api_can_create_a_product()
        response = self.client.get('/products/avl/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Iphone 8')
        self.assertContains(response, 'Iphone 7')

    def test_api_can_post_purchase_product(self):
        """Test the api to purchase single product."""
        self.test_api_can_create_a_product()
        self.assertEqual(Product.objects.get(title='Iphone 7').inventory_count, 25)
        response = self.client.post('/products/1/purchase/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.get(title='Iphone 7').inventory_count, 24)

    def test_api_can_post_cart_product(self):
        """Test the api to add product to cart."""
        self.test_api_can_create_a_product()
        self.assertEqual(Cart.objects.count(), 0)
        response = self.client.post('/products/1/addcart/', json.dumps(
            {"product": "Iphone 7", "price": 800, "product_cnt": 1, "checked_out": False, "owner": 1}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Cart.objects.count(), 1)

    def test_api_can_get_cart(self):
        """Test the api can get Cart."""
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Total Amount')

    def test_api_can_post_cart_checkout(self):
        """Test the api to checkout to cart."""
        response = self.client.post('/cart/checkout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Cart.objects.count(), 0)
