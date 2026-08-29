from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart for user {self.user.username}"
        return f"Anonymous Cart {self.session_key}"

    @property
    def get_total_price(self):
        return sum(item.get_subtotal for item in self.items.all())

    @property
    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=20, default='M')
    color = models.CharField(max_length=50, default='Black')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_subtotal(self):
        return self.product.get_price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.size} / {self.color})"

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs):
    session_key = request.session.session_key
    if session_key:
        session_cart = Cart.objects.filter(session_key=session_key).first()
        if session_cart:
            user_cart, created = Cart.objects.get_or_create(user=user)
            for item in session_cart.items.all():
                existing_item = user_cart.items.filter(
                    product=item.product, size=item.size, color=item.color
                ).first()
                if existing_item:
                    existing_item.quantity += item.quantity
                    existing_item.save()
                    item.delete()
                else:
                    item.cart = user_cart
                    item.save()
            session_cart.delete()

