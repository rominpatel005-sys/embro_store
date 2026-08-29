from cart.models import Cart

def cart_count(request):
    total_count = 0
    wishlist_count = 0
    
    if request.user.is_authenticated:
        # Calculate cart items for authenticated user
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            total_count = cart.get_total_items
        # Calculate wishlist items
        wishlist_count = request.user.wishlist_items.count()
    else:
        # Calculate cart items for guest user using sessions
        session_key = request.session.session_key
        if not session_key:
            # We don't want to create a full session record just to get a key, 
            # but if it doesn't exist, we know the cart count is 0.
            pass
        else:
            cart = Cart.objects.filter(session_key=session_key).first()
            if cart:
                total_count = cart.get_total_items
                
    return {
        'cart_count': total_count,
        'wishlist_count': wishlist_count
    }
