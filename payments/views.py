import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from orders.models import Order
from cart.models import Cart
from .models import Payment

@login_required
def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Check if payment already exists
    payment, created = Payment.objects.get_or_create(
        order=order,
        defaults={
            'payment_method': request.session.get('pending_payment_method', 'UPI'),
            'amount': order.total_amount,
            'status': 'PENDING'
        }
    )
    
    if payment.status == 'PAID':
        messages.warning(request, "This order has already been paid for.")
        return redirect('orders:order_detail', order_id=order.id)

    if request.method == 'POST':
        action = request.POST.get('action') # 'success' or 'fail'
        payment_method = request.POST.get('payment_method', payment.payment_method)
        
        payment.payment_method = payment_method
        payment.transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        
        if action == 'success':
            payment.status = 'PAID'
            payment.save()
            
            # Update order status to CONFIRMED
            order.status = 'CONFIRMED'
            order.save()
            
            # Clear user cart
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                cart.items.all().delete()
                
            messages.success(request, f"Simulated online payment of ${order.total_amount} successful! Transaction ID: {payment.transaction_id}")
            return redirect('orders:order_detail', order_id=order.id)
        else:
            payment.status = 'FAILED'
            payment.save()
            messages.error(request, "Simulated online payment failed. Please try again or select Cash on Delivery.")
            return render(request, 'payments/payment_failed.html', {'order': order, 'payment': payment})

    context = {
        'order': order,
        'payment': payment,
        'payment_method': payment.payment_method,
    }
    return render(request, 'payments/process_payment.html', context)
