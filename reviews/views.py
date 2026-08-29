from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Review
from .forms import ReviewForm

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.approved = False # Needs admin approval
            review.save()
            messages.success(request, "Your review has been submitted successfully and is awaiting administrator approval.")
        else:
            messages.error(request, "There was an error in your review submission.")
    return redirect('products:product_detail', slug=product.slug)
