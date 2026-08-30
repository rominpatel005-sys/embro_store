from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from products.models import Category, Product


class ApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('buyer', password='A-secure-test-password-123')
        category = Category.objects.create(name='Test', gender='UNISEX')
        self.product = Product.objects.create(
            name='Test Shirt', description='Test product', price=100,
            category=category, stock=3, sizes='M,L', colors='Black,White'
        )

    def authenticate(self):
        response = self.client.post('/api/auth/login/', {'username': 'buyer', 'password': 'A-secure-test-password-123'})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_catalog_is_public(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_cart_validates_variant(self):
        self.authenticate()
        response = self.client.post('/api/cart/', {
            'product': self.product.id, 'quantity': 1, 'size': 'XXL', 'color': 'Black'
        })
        self.assertEqual(response.status_code, 400)

    def test_checkout_creates_order_and_reduces_stock(self):
        self.authenticate()
        self.client.post('/api/cart/', {
            'product': self.product.id, 'quantity': 2, 'size': 'M', 'color': 'Black'
        })
        response = self.client.post('/api/checkout/', {
            'full_name': 'Test Buyer', 'mobile': '9999999999', 'email': 'buyer@example.com',
            'address': 'Test address', 'state': 'Gujarat', 'city': 'Ahmedabad',
            'pincode': '380001', 'payment_method': 'COD'
        })
        self.assertEqual(response.status_code, 201)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 1)
