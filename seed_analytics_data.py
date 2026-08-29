import os
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'faction_store.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserLoginHistory
from products.models import Product
from orders.models import Order, OrderItem
from payments.models import Payment

def seed_analytics():
    print("Starting seed analytics data...")
    
    # 1. Ensure test users exist
    test_usernames = ['alice', 'bob', 'charlie', 'diana', 'elise', 'frank', 'grace', 'henry']
    users = []
    for username in test_usernames:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': f"{username}@example.com",
                'first_name': username.capitalize(),
                'last_name': 'Test'
            }
        )
        if created:
            user.set_password('password123')
            user.save()
        users.append(user)
        
    all_users = list(User.objects.all())
    if not all_users:
        print("No users found and failed to create test users.")
        return
        
    # 2. Seed Login History over the last 30 days
    print("Seeding login history...")
    # Clear existing logins to make it clean
    UserLoginHistory.objects.all().delete()
    
    ips = ['192.168.1.10', '192.168.1.11', '192.168.1.12', '203.0.113.195', '198.51.100.4', '203.0.113.50', '8.8.8.8']
    
    now = timezone.now()
    logins_to_create = []
    
    for day_offset in range(30, -1, -1):
        target_date = now - timedelta(days=day_offset)
        # Random number of logins per day: 3 to 12
        num_logins = random.randint(3, 12)
        for _ in range(num_logins):
            user = random.choice(all_users)
            ip = random.choice(ips)
            # Create object in memory first
            login_event = UserLoginHistory(
                user=user,
                ip_address=ip
            )
            logins_to_create.append((login_event, target_date))
            
    # Bulk create
    instances = [item[0] for item in logins_to_create]
    UserLoginHistory.objects.bulk_create(instances)
    
    # Update timestamps (since auto_now_add overrides the constructor setting)
    created_events = list(UserLoginHistory.objects.all().order_by('id'))
    for idx, (login_event, target_date) in enumerate(logins_to_create):
        # We match them in order
        db_event = created_events[idx]
        # Set a random hour/minute
        random_time = target_date.replace(
            hour=random.randint(0, 23),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )
        UserLoginHistory.objects.filter(id=db_event.id).update(timestamp=random_time)
        
    print(f"Seeded {len(logins_to_create)} user logins.")

    # 3. Seed Orders if there are products
    existing_products = list(Product.objects.all())
    if not existing_products:
        print("Warning: No products found in the catalog. Cannot seed orders.")
        return
        
    print("Clearing and re-seeding orders to populate charts...")
    # Clear existing orders first to have clean stats for testing
    Order.objects.all().delete()
    
    states_cities = [
        ('New York', 'New York City', '10001'),
        ('California', 'Los Angeles', '90001'),
        ('Texas', 'Houston', '77001'),
        ('Illinois', 'Chicago', '60601'),
        ('Florida', 'Miami', '33101')
    ]
    
    sizes = ['S', 'M', 'L', 'XL']
    colors = ['Black', 'White', 'Navy Blue', 'Crimson Red', 'Heather Grey']
    
    orders_to_seed = 35
    for i in range(orders_to_seed, -1, -1):
        order_date = now - timedelta(days=i)
        user = random.choice(all_users)
        state_info = random.choice(states_cities)
        
        # Determine items in this order: 1 to 3 items
        num_items = random.randint(1, 3)
        order_items_data = []
        total_amount = 0
        
        for _ in range(num_items):
            prod = random.choice(existing_products)
            qty = random.randint(1, 3)
            size = random.choice(prod.sizes.split(',')) if prod.sizes else random.choice(sizes)
            color = random.choice(prod.colors.split(',')) if prod.colors else random.choice(colors)
            price = prod.get_price
            
            subtotal = price * qty
            total_amount += subtotal
            
            order_items_data.append({
                'product': prod,
                'product_name': prod.name,
                'price': price,
                'quantity': qty,
                'size': size,
                'color': color
            })
            
        # Create order
        status = random.choices(
            ['DELIVERED', 'SHIPPED', 'CONFIRMED', 'PENDING', 'CANCELLED'],
            weights=[60, 15, 10, 10, 5],
            k=1
        )[0]
        
        order = Order.objects.create(
            user=user,
            full_name=f"{user.first_name} {user.last_name}",
            mobile=f"+1 {random.randint(100, 999)}-555-{random.randint(1000, 9999)}",
            email=user.email,
            address=f"{random.randint(100, 999)} Fashion Ave",
            state=state_info[0],
            city=state_info[1],
            pincode=state_info[2],
            total_amount=total_amount,
            status=status
        )
        
        # Override created_at for orders
        random_time = order_date.replace(
            hour=random.randint(0, 23),
            minute=random.randint(0, 59)
        )
        Order.objects.filter(id=order.id).update(created_at=random_time)
        
        # Create Order Items
        for item_data in order_items_data:
            OrderItem.objects.create(
                order=order,
                product=item_data['product'],
                product_name=item_data['product_name'],
                price=item_data['price'],
                quantity=item_data['quantity'],
                size=item_data['size'],
                color=item_data['color']
            )
            
        # Create Payment
        pay_status = 'PAID' if status in ['DELIVERED', 'SHIPPED', 'CONFIRMED'] else 'PENDING'
        if status == 'CANCELLED':
            pay_status = random.choice(['PENDING', 'FAILED'])
            
        payment_method = random.choice(['CREDIT_CARD', 'UPI', 'COD', 'NET_BANKING'])
        Payment.objects.create(
            order=order,
            payment_method=payment_method,
            transaction_id=f"TXN{random.randint(10000000, 99999999)}",
            amount=total_amount,
            status=pay_status
        )
        
    print(f"Seeded {orders_to_seed} orders and payments successfully.")

if __name__ == '__main__':
    seed_analytics()
