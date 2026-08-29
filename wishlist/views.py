from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from products.models import Product
from .models import Wishlist

@login_required
def wishlist_list(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist_detail.html', {'wishlist': wishlist})

@login_required
def wishlist_toggle(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
    
    if wishlist_item:
        wishlist_item.delete()
        added = False
        message = f"{product.name} removed from wishlist."
    else:
        Wishlist.objects.create(user=request.user, product=product)
        added = True
        message = f"{product.name} added to wishlist."

    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'added': added,
            'message': message,
            'wishlist_count': wishlist_count,
        })
    return redirect('wishlist:wishlist_list')
