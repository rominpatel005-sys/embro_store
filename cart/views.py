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

import base64
import uuid
from django.core.files.base import ContentFile

@require_POST
def cart_add(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('size', 'M')
    color = request.POST.get('color', 'Black')
    
    # Handle custom design image (uploaded file or base64 data)
    custom_image_file = request.FILES.get('custom_image')
    if not custom_image_file:
        b64_data = request.POST.get('custom_image_base64') or request.POST.get('custom_image')
        if b64_data and 'base64,' in b64_data:
            try:
                format_part, imgstr = b64_data.split(';base64,')
                ext = format_part.split('/')[-1] if '/' in format_part else 'png'
                if ext.lower() in ['jpeg', 'jpg']:
                    ext = 'jpg'
                else:
                    ext = 'png'
                file_name = f"custom_design_{uuid.uuid4().hex[:10]}.{ext}"
                custom_image_file = ContentFile(base64.b64decode(imgstr), name=file_name)
            except Exception:
                pass
        elif b64_data and len(b64_data) > 100 and not b64_data.startswith('http'):
            try:
                file_name = f"custom_design_{uuid.uuid4().hex[:10]}.png"
                custom_image_file = ContentFile(base64.b64decode(b64_data), name=file_name)
            except Exception:
                pass

    # Check if stock is available
    if product.stock < quantity:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Not enough stock available.'})
        return redirect('products:product_detail', slug=product.slug)

    # If this is a custom design, create a dedicated cart item so it's not merged with standard items
    if custom_image_file:
        cart_item = CartItem.objects.create(
            cart=cart,
            product=product,
            size=size,
            color=color,
            quantity=quantity,
            custom_image=custom_image_file
        )
    else:
        # Standard item: Check if item already exists in cart with same size/color (and no custom image)
        existing_item = cart.items.filter(
            product=product, size=size, color=color, custom_image__in=['', None]
        ).first()
        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
            cart_item = existing_item
        else:
            cart_item = CartItem.objects.create(
                cart=cart, product=product, size=size, color=color, quantity=quantity
            )

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
