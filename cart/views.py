from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from products.models import Product
from .models import Cart, CartItem

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def cart_detail(request):
    cart = get_or_create_cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@require_POST
def cart_add(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('size', 'M')
    color = request.POST.get('color', 'Black')
    
    # Check if stock is available
    if product.stock < quantity:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Not enough stock available.'})
        return redirect('products:product_detail', slug=product.slug)

    # Check if item already exists in cart with same size/color
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, size=size, color=color,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f"{product.name} added to cart.",
            'cart_count': cart.get_total_items,
            'cart_total': str(cart.get_total_price),
        })
    return redirect('cart:cart_detail')

@require_POST
def cart_update(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        cart_item.delete()
        message = "Item removed from cart."
        item_deleted = True
    else:
        # Check stock limits
        if cart_item.product.stock < quantity:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Not enough stock available.'})
            return redirect('cart:cart_detail')
            
        cart_item.quantity = quantity
        cart_item.save()
        message = "Cart updated."
        item_deleted = False

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': message,
            'item_deleted': item_deleted,
            'item_subtotal': str(cart_item.get_subtotal) if not item_deleted else '0.00',
            'cart_count': cart.get_total_items,
            'cart_total': str(cart.get_total_price),
        })
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f"{product_name} removed from cart.",
            'cart_count': cart.get_total_items,
            'cart_total': str(cart.get_total_price),
        })
    return redirect('cart:cart_detail')
