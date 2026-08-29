from django.db import models
from orders.models import Order

PAYMENT_METHOD_CHOICES = (
    ('COD', 'Cash On Delivery'),
    ('UPI', 'UPI Payment'),
    ('CREDIT_CARD', 'Credit Card'),
    ('DEBIT_CARD', 'Debit Card'),
    ('NET_BANKING', 'Net Banking'),
)

PAYMENT_STATUS_CHOICES = (
    ('PENDING', 'Pending'),
    ('PAID', 'Paid'),
    ('FAILED', 'Failed'),
)

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default='COD')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} for Order #{self.order.id} - Status: {self.status}"
