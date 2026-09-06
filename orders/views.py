from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from cart.models import Cart
from payments.models import Payment
from .models import Order, OrderItem
from .forms import OrderCreateForm

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or cart.items.count() == 0:
        messages.warning(request, "Your cart is empty. Add products to checkout.")
        return redirect('cart:cart_detail')
        
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            try:
                # Wrap inside database transaction to ensure atomicity
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.user = request.user
                    order.total_amount = cart.get_total_price
                    order.save()
                    
                    # Create Order Items and decrease stock
                    for item in cart.items.all():
                        product = item.product
                        if product.stock < item.quantity:
                            raise ValueError(f"Sorry, {product.name} is out of stock.")
                            
                        product.stock -= item.quantity
                        product.save()
                        
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            product_name=product.name,
                            price=product.get_price,
                            quantity=item.quantity,
                            size=item.size,
                            color=item.color
                        )
                    
                    payment_method = form.cleaned_data.get('payment_method')
                    
                    if payment_method == 'COD':
                        # COD Order: Save payment as pending, complete order setup, clear cart
                        Payment.objects.create(
                            order=order,
                            payment_method='COD',
                            amount=order.total_amount,
                            status='PENDING'
                        )
                        cart.items.all().delete()
                        messages.success(request, f"Order #{order.id} placed successfully using Cash on Delivery.")
                        return redirect('orders:order_detail', order_id=order.id)
                    else:
                        # Online Payment: Redirect to payments gateway page
                        request.session['pending_order_id'] = order.id
                        request.session['pending_payment_method'] = payment_method
                        return redirect('payments:process_payment', order_id=order.id)
                        
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
    else:
        # Prepopulate shipping details from UserProfile if exists
        profile = request.user.profile
        form = OrderCreateForm(initial={
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip(),
            'email': request.user.email,
            'mobile': profile.mobile,
            'address': profile.address,
            'state': profile.state,
            'city': profile.city,
            'pincode': profile.pincode
        })
        
    return render(request, 'orders/checkout.html', {'form': form, 'cart': cart})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    if request.user.is_staff:
        order = get_object_or_404(Order, id=order_id)
    else:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_cancel(request, order_id):
    if request.user.is_staff:
        order = get_object_or_404(Order, id=order_id)
    else:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.is_cancellable:
        with transaction.atomic():
            order.status = 'CANCELLED'
            order.save()
            
            # Restock items
            for item in order.items.all():
                if item.product:
                    item.product.stock += item.quantity
                    item.product.save()
                    
            messages.success(request, f"Order #{order.id} has been cancelled and items have been restocked.")
    else:
        messages.error(request, f"Order #{order.id} cannot be cancelled as it is already {order.get_status_display()}.")
    return redirect('orders:order_detail', order_id=order.id)
