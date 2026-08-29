import os
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, Product
from reviews.models import Review
from orders.models import Order, OrderItem
from payments.models import Payment
from dashboard.models import Settings
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Seed the database with realistic sample fashion products, users, reviews, and orders'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Starting database seeding..."))

        # 1. Create Store Settings if not exists
        Settings.get_settings()
        self.stdout.write(self.style.SUCCESS("[OK] Store settings checked/created."))

        # 2. Create Sample Users
        users_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'emma_watson', 'email': 'emma@example.com', 'first_name': 'Emma', 'last_name': 'Watson'},
        ]
        
        users = []
        for u in users_data:
            user, created = User.objects.get_or_create(
                username=u['username'],
                defaults={
                    'email': u['email'],
                    'first_name': u['first_name'],
                    'last_name': u['last_name']
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                # Update profile
                profile = user.profile
                profile.mobile = f"98765{random.randint(10000, 99999)}"
                profile.city = random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston'])
                profile.state = random.choice(['NY', 'CA', 'IL', 'TX'])
                profile.address = "123 Test St"
                profile.pincode = "100001"
                profile.email_verified = True
                profile.save()
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f"[OK] {len(users)} test users checked/created."))

        # 3. Fetch/Verify Categories
        categories = {c.name + "_" + c.gender: c for c in Category.objects.all()}
        if not categories:
            self.stdout.write(self.style.ERROR("No categories found in database. Run migrations first!"))
            return

        # 4. Create Sample Products
        products_data = [
            # Men
            {
                'name': 'Slim Fit Linen Shirt',
                'category_key': 'Shirts_MEN',
                'description': 'A premium quality linen shirt, perfect for casual summer wear. Features a slim fit, button-down collar, and breathable fabric.',
                'price': 49.99,
                'discount_price': 39.99,
                'brand': 'Embro Premium',
                'stock': 25,
                'sizes': 'S,M,L,XL',
                'colors': 'White,Light Blue,Navy',
            },
            {
                'name': 'Graphic Streetwear Hoodie',
                'category_key': 'Hoodies_MEN',
                'description': 'Over-sized graphic print hoodie. Made with thick loopback cotton fleece for maximum comfort and style.',
                'price': 79.99,
                'discount_price': None,
                'brand': 'Embro Street',
                'stock': 15,
                'sizes': 'M,L,XL',
                'colors': 'Black,Sage Green',
            },
            {
                'name': 'Classic Denim Jacket',
                'category_key': 'Jackets_MEN',
                'description': 'A timeless raw denim jacket that ages beautifully. Features button closure, chest pockets, and adjustable waist tabs.',
                'price': 119.99,
                'discount_price': 99.99,
                'brand': 'Embro Denim',
                'stock': 12,
                'sizes': 'S,M,L,XL,XXL',
                'colors': 'Dark Blue,Light Wash',
            },
            {
                'name': 'Vintage Wash Relaxed Jeans',
                'category_key': 'Jeans_MEN',
                'description': 'Relaxed fit jeans crafted from 100% organic cotton denim. Finished with a vintage wash for a broken-in look.',
                'price': 89.99,
                'discount_price': None,
                'brand': 'Embro Denim',
                'stock': 30,
                'sizes': '30,32,34,36',
                'colors': 'Indigo,Light Grey',
            },
            {
                'name': 'Classic Crewneck T-Shirt',
                'category_key': 'T-Shirts_MEN',
                'description': 'Super-soft combed cotton basic crewneck. Designed for daily layering or standalone wear.',
                'price': 24.99,
                'discount_price': 19.99,
                'brand': 'Embro Basics',
                'stock': 50,
                'sizes': 'S,M,L,XL',
                'colors': 'Black,White,Heather Grey',
            },
            # Women
            {
                'name': 'Ribbed Knit Crop Top',
                'category_key': 'Tops_WOMEN',
                'description': 'Sleek ribbed knit crop top with a square neckline. High stretch and body-hugging silhouette.',
                'price': 29.99,
                'discount_price': None,
                'brand': 'Embro Studio',
                'stock': 40,
                'sizes': 'XS,S,M,L',
                'colors': 'Beige,Black,Dusty Rose',
            },
            {
                'name': 'Floral Summer Midi Dress',
                'category_key': 'Dresses_WOMEN',
                'description': 'Lightweight floral print midi dress featuring adjustable spaghetti straps and a side thigh slit. Elegant and breezy.',
                'price': 69.99,
                'discount_price': 59.99,
                'brand': 'Embro Studio',
                'stock': 18,
                'sizes': 'XS,S,M,L,XL',
                'colors': 'Red Floral,Blue Floral',
            },
            {
                'name': 'Cozy Knit Oversized Hoodie',
                'category_key': 'Hoodies_WOMEN',
                'description': 'Ultra-soft fleece oversized hoodie with drop shoulders and a spacious front pocket. Your go-to lounge companion.',
                'price': 59.99,
                'discount_price': 49.99,
                'brand': 'Embro Basics',
                'stock': 22,
                'sizes': 'S,M,L',
                'colors': 'Cream,Oatmeal,Charcoal',
            },
            {
                'name': 'High-Waisted Wide Leg Jeans',
                'category_key': 'Jeans_WOMEN',
                'description': 'Modern high-rise wide-leg jeans in premium rigid denim. Flatters the waist and extends the leg line.',
                'price': 99.99,
                'discount_price': None,
                'brand': 'Embro Denim',
                'stock': 20,
                'sizes': '26,27,28,29,30',
                'colors': 'Stonewash,Ecru',
            },
            {
                'name': 'Faux Leather Biker Jacket',
                'category_key': 'Jackets_WOMEN',
                'description': 'Classic biker jacket in high-quality buttery soft faux leather. Complete with asymmetric zip and silver hardware.',
                'price': 149.99,
                'discount_price': 129.99,
                'brand': 'Embro Premium',
                'stock': 8,
                'sizes': 'S,M,L',
                'colors': 'Black,Espresso',
            }
        ]

        products = []
        for p in products_data:
            cat = categories.get(p['category_key'])
            if not cat:
                continue
            
            product, created = Product.objects.get_or_create(
                name=p['name'],
                defaults={
                    'category': cat,
                    'description': p['description'],
                    'price': p['price'],
                    'discount_price': p['discount_price'],
                    'brand': p['brand'],
                    'stock': p['stock'],
                    'sizes': p['sizes'],
                    'colors': p['colors']
                }
            )
            products.append(product)
        self.stdout.write(self.style.SUCCESS(f"[OK] {len(products)} fashion products checked/created."))

        # 5. Create Sample Reviews
        comments = [
            "Extremely comfortable! The fabric is high quality and it fits perfectly.",
            "Love the design and the color is exactly as shown. Highly recommend!",
            "Great value for money. Very stylish.",
            "Decent purchase, but the sizing runs slightly small. Consider ordering a size up.",
            "Absolutely stunning piece! Fast delivery and great customer service."
        ]

        review_count = 0
        for p in products:
            if Review.objects.filter(product=p).exists():
                continue
            
            # Add 2 reviews per product
            review_users = random.sample(users, 2)
            for ru in review_users:
                rating = random.choice([4, 5])
                Review.objects.create(
                    product=p,
                    user=ru,
                    rating=rating,
                    comment=random.choice(comments),
                    approved=True
                )
                review_count += 1
        self.stdout.write(self.style.SUCCESS(f"[OK] {review_count} product reviews created."))

        # 6. Create Sample Orders
        order_count = 0
        if not Order.objects.exists():
            for i in range(5):
                ru = random.choice(users)
                order_products = random.sample(products, random.randint(1, 2))
                
                # Create Order
                order = Order.objects.create(
                    user=ru,
                    full_name=f"{ru.first_name} {ru.last_name}",
                    mobile=ru.profile.mobile,
                    email=ru.email,
                    address=ru.profile.address,
                    city=ru.profile.city,
                    state=ru.profile.state,
                    pincode=ru.profile.pincode,
                    total_amount=0, # Will update based on items
                    status=random.choice(['PENDING', 'CONFIRMED', 'DELIVERED'])
                )
                
                total = 0
                for op in order_products:
                    qty = random.randint(1, 2)
                    price = op.get_price
                    subtotal = price * qty
                    total += subtotal
                    
                    OrderItem.objects.create(
                        order=order,
                        product=op,
                        product_name=op.name,
                        price=price,
                        quantity=qty,
                        size=random.choice(op.sizes.split(',')),
                        color=random.choice(op.colors.split(','))
                    )
                
                order.total_amount = total
                order.save()
                
                # Create Payment
                Payment.objects.create(
                    order=order,
                    payment_method=random.choice(['COD', 'UPI', 'CREDIT_CARD']),
                    amount=total,
                    status='PAID' if order.status in ['CONFIRMED', 'DELIVERED'] else 'PENDING',
                    transaction_id=f"TXN{random.randint(10000000, 99999999)}"
                )
                order_count += 1
            self.stdout.write(self.style.SUCCESS(f"[OK] {order_count} past orders & payments simulated."))

        self.stdout.write(self.style.SUCCESS("[OK] Seeding completed successfully!"))
