from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Product, Category
from reviews.models import Review
from orders.models import Order

def home(request):
    User = get_user_model()

    # Featured: high rating, Trending: latest, Best Sellers: default limit
    featured_products = Product.objects.filter(rating__gte=4.0)[:8]
    trending_products = Product.objects.order_by('-created_at')[:8]
    best_sellers = Product.objects.filter(stock__gt=0)[:8]
    latest_collection = Product.objects.order_by('-created_at')[:8]
    
    # Retrieve the 10 seeded 3D animation products
    animated_products = Product.objects.filter(slug__in=[
        'elephant-embroidered-black-t-shirt',
        'tropical-palms-brown-t-shirt',
        'marvel-icons-cream-t-shirt',
        'snoopy-chill-maroon-t-shirt',
        'royal-enfield-cream-t-shirt',
        'majestic-stag-black-t-shirt',
        'marvel-team-cream-t-shirt',
        'tropical-palms-espresso-t-shirt',
        'forest-deer-black-t-shirt',
        'running-stallion-black-t-shirt'
    ])
    
    # Approved reviews to show on home page
    customer_reviews = Review.objects.filter(approved=True).order_by('-created_at')[:6]
    
    # Dynamic counts driven by actual database records
    total_products = Product.objects.count()
    total_users = User.objects.count()
    total_orders = Order.objects.count()

    context = {
        'featured_products': featured_products,
        'trending_products': trending_products,
        'best_sellers': best_sellers,
        'latest_collection': latest_collection,
        'customer_reviews': customer_reviews,
        'animated_products': animated_products,
        'total_products': total_products,
        'total_users': total_users,
        'total_orders': total_orders,
    }
    return render(request, 'products/home.html', context)

def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    
    # Filtering
    query = request.GET.get('q')
    gender = request.GET.get('gender')
    category_slug = request.GET.get('category')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    brand = request.GET.get('brand')
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(brand__icontains=query)
        )
        
    if gender:
        products = products.filter(category__gender=gender.upper())
        
    if category_slug:
        products = products.filter(category__slug=category_slug)
        
    if price_min:
        try:
            products = products.filter(price__gte=float(price_min))
        except ValueError:
            pass
            
    if price_max:
        try:
            products = products.filter(price__lte=float(price_max))
        except ValueError:
            pass
            
    if brand:
        products = products.filter(brand__iexact=brand)
        
    # Sorting
    sort_by = request.GET.get('sort')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    elif sort_by == 'latest':
        products = products.order_by('-created_at')

    # Distinct list of brands for filtering
    all_brands = Product.objects.values_list('brand', flat=True).distinct()
    
    # Pagination
    paginator = Paginator(products, 12) # 12 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'all_brands': all_brands,
        'selected_category': category_slug,
        'selected_gender': gender,
        'selected_brand': brand,
        'price_min': price_min,
        'price_max': price_max,
        'sort_by': sort_by,
        'query': query,
    }
    return render(request, 'products/catalog.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    # Related products (same category, excluding current, limit to 4)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    # Approved reviews for this product
    reviews = Review.objects.filter(product=product, approved=True)
    
    # Split sizes and colors for template checkboxes/dropdowns
    product_sizes = [s.strip() for s in product.sizes.split(',') if s.strip()]
    product_colors = [c.strip() for c in product.colors.split(',') if c.strip()]
    
    # Track recently viewed in sessions
    recently_viewed = request.session.get('recently_viewed', [])
    if product.id in recently_viewed:
        recently_viewed.remove(product.id)
    recently_viewed.insert(0, product.id)
    recently_viewed = recently_viewed[:5] # Keep last 5 items
    request.session['recently_viewed'] = recently_viewed
    
    # Fetch recently viewed products from DB
    viewed_ids = [pid for pid in recently_viewed if pid != product.id]
    recently_viewed_products = []
    if viewed_ids:
        db_products = Product.objects.filter(id__in=viewed_ids)
        # Re-sort to maintain order of viewed_ids
        recently_viewed_products = sorted(db_products, key=lambda x: viewed_ids.index(x.id))
        
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'product_sizes': product_sizes,
        'product_colors': product_colors,
        'recently_viewed_products': recently_viewed_products,
    }
    return render(request, 'products/detail.html', context)

def ajax_search(request):
    query = request.GET.get('q', '')
    results = []
    if len(query) >= 2:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(brand__icontains=query) | Q(category__name__icontains=query)
        )[:6]
        for p in products:
            results.append({
                'name': p.name,
                'brand': p.brand,
                'slug': p.slug,
                'price': str(p.get_price),
                'image_url': p.image.url if p.image else '/static/images/placeholder.jpg',
            })
    return JsonResponse({'results': results})

@login_required
def custom_design(request):
    tshirts = Product.objects.filter(
        Q(category__name__icontains='T-Shirt') | Q(name__icontains='T-Shirt')
    ).distinct()
    return render(request, 'products/custom_design.html', {'tshirts': tshirts})
