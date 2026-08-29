from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from accounts.models import UserLoginHistory
from products.models import Product, Category
from orders.models import Order, OrderItem

class AnalyticsDashboardTests(TestCase):
    def setUp(self):
        # Create categories and products
        self.category = Category.objects.create(name="T-Shirt", gender="MEN")
        self.product = Product.objects.create(
            name="Classic Polo Shirt",
            price=29.99,
            category=self.category,
            sizes="S,M,L",
            colors="Blue,Black"
        )
        
        # Create users
        self.staff_user = User.objects.create_user(
            username="staff_admin",
            password="adminpassword",
            email="staff@example.com",
            is_staff=True
        )
        self.normal_user = User.objects.create_user(
            username="customer_john",
            password="customerpassword",
            email="john@example.com"
        )
        
        # Create login history
        UserLoginHistory.objects.create(user=self.normal_user, ip_address="192.168.1.1")
        
        # Create an order and order items
        self.order = Order.objects.create(
            user=self.normal_user,
            full_name="John Doe",
            mobile="1234567890",
            email="john@example.com",
            address="123 Street",
            state="NY",
            city="New York",
            pincode="10001",
            total_amount=59.98,
            status="DELIVERED"
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            product_name=self.product.name,
            price=self.product.price,
            quantity=2,
            size="M",
            color="Blue"
        )
        
        # Initialize client
        self.client = Client()

    def test_anonymous_user_redirected(self):
        url = reverse('dashboard:analytics')
        response = self.client.get(url)
        # staff_member_required redirects to login
        self.assertEqual(response.status_code, 302)

    def test_non_staff_user_redirected(self):
        url = reverse('dashboard:analytics')
        self.client.login(username="customer_john", password="customerpassword")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_staff_user_access_and_context(self):
        url = reverse('dashboard:analytics')
        self.client.login(username="staff_admin", password="adminpassword")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/analytics.html')
        
        # Check context keys exist
        self.assertIn('login_labels', response.context)
        self.assertIn('login_counts', response.context)
        self.assertIn('logins_today', response.context)
        self.assertIn('popular_apparel', response.context)
        self.assertIn('top_buyers', response.context)
        self.assertIn('best_selling_variant', response.context)
        self.assertIn('top_buyer', response.context)
        
        # Check login trend calculations (should include our login history)
        # Since we added 1 login for customer_john today, logins_today should be at least 1
        # (plus any logins from automatic logs during tests)
        self.assertGreaterEqual(response.context['logins_today'], 1)
        
        # Check popular apparel totals
        popular_items = response.context['popular_apparel']
        self.assertEqual(len(popular_items), 1)
        self.assertEqual(popular_items[0]['product_name'], "Classic Polo Shirt")
        self.assertEqual(popular_items[0]['size'], "M")
        self.assertEqual(popular_items[0]['total_sold'], 2)
        
        # Check top buyer details
        top_buyers = response.context['top_buyers']
        self.assertEqual(len(top_buyers), 1)
        self.assertEqual(top_buyers[0]['order__user__username'], "customer_john")
        self.assertEqual(top_buyers[0]['total_spent'], Decimal('59.98'))

