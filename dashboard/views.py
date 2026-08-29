from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum, Count, F, Avg
from django.db.models.functions import TruncDay
from django.db import models, transaction
from django.utils import timezone
from datetime import timedelta
from products.models import Product, Category, ProductImage
from orders.models import Order, OrderItem
from reviews.models import Review
from contacts.models import ContactMessage
from accounts.models import UserLoginHistory
from .models import Settings, DashboardWidget
from .forms import ProductForm, CategoryForm, SettingsForm
from django.http import JsonResponse
import json

def _seed_default_widgets():
    defaults = [
        # Cards
        {
            'key': 'revenue',
            'title': 'Total Revenue',
            'widget_type': 'CARD',
            'subtitle': 'Paid transactions',
            'icon': 'fas fa-check-circle',
            'text_color': '#ffc107',
            'bg_color': 'rgba(18, 18, 22, 0.55)',
            'border_color': 'rgba(255, 255, 255, 0.08)',
        },
        {
            'key': 'orders',
            'title': 'Total Orders',
            'widget_type': 'CARD',
            'subtitle': 'All checkout drops',
            'icon': 'fas fa-shopping-bag',
            'text_color': '#ffffff',
            'bg_color': 'rgba(18, 18, 22, 0.55)',
            'border_color': 'rgba(255, 255, 255, 0.08)',
        },
        {
            'key': 'products',
            'title': 'Products In Catalog',
            'widget_type': 'CARD',
            'subtitle': 'Add Apparel',
            'icon': 'fas fa-plus',
            'text_color': '#ffffff',
            'bg_color': 'rgba(18, 18, 22, 0.55)',
            'border_color': 'rgba(255, 255, 255, 0.08)',
        },
        {
            'key': 'clients',
            'title': 'Registered Clients',
            'widget_type': 'CARD',
            'subtitle': 'Excluding administrators',
            'icon': 'fas fa-users',
            'text_color': '#ffffff',
            'bg_color': 'rgba(18, 18, 22, 0.55)',
            'border_color': 'rgba(255, 255, 255, 0.08)',
        },
        # Charts
        {
            'key': 'category_chart',
            'title': 'Categories Share',
            'widget_type': 'CHART',
            'chart_type': 'PIE',
            'subtitle': 'Products distribution',
            'icon': 'fas fa-chart-pie',
            'bg_color': 'rgba(18, 18, 22, 0.55)',
            'border_color': 'rgba(255, 255, 255, 0.08)',
            'colors_json': '["#d4af37", "#ffaa00", "#3b82f6", "#10b981", "#ef4444", "#a855f7"]',
        },
        {
            'key': 'status_chart',
            'title': 'Order Statuses',
            'widget_type': 'CHART',
            'chart_type': 'BAR',
            'subtitle': 'Order status distribution',
            'icon': 'fas fa-chart-bar',
            'bg_color': 'rgba(18, 18, 22, 0.55)',
            'border_color': 'rgba(255, 255, 255, 0.08)',
            'colors_json': '["#d4af37", "#ffaa00", "#3b82f6", "#10b981", "#ef4444", "#a855f7"]',
        },
    ]
    for pos, w in enumerate(defaults):
        DashboardWidget.objects.get_or_create(
            key=w['key'],
            defaults={
                'title': w['title'],
                'widget_type': w['widget_type'],
                'chart_type': w.get('chart_type'),
                'subtitle': w.get('subtitle'),
                'icon': w.get('icon', 'fas fa-chart-bar'),
                'text_color': w.get('text_color', '#ffffff'),
                'bg_color': w.get('bg_color', 'rgba(18, 18, 22, 0.55)'),
                'border_color': w.get('border_color', 'rgba(255, 255, 255, 0.08)'),
                'position': pos,
                'colors_json': w.get('colors_json', '["#d4af37", "#ffaa00", "#3b82f6", "#10b981", "#ef4444", "#a855f7"]'),
            }
        )

def _get_dashboard_context():
    # --- ORIGINAL OVERVIEW STATS ---
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_customers = User.objects.filter(is_staff=False).count()
    
    # Revenue from paid orders
    total_revenue_dict = Order.objects.filter(payment__status='PAID').aggregate(total=Sum('total_amount'))
    total_revenue = total_revenue_dict['total'] if total_revenue_dict['total'] is not None else 0.00
    
    recent_orders = Order.objects.all().order_by('-created_at')[:10]
    low_stock_products = Product.objects.filter(stock__lt=5)
    
    # Chart Data: Categories Share
    category_chart_data = Category.objects.annotate(prod_count=Count('products')).values('name', 'prod_count')
    category_labels = [c['name'] for c in category_chart_data]
    category_counts = [c['prod_count'] for c in category_chart_data]
    
    # Chart Data: Order Status counts
    order_status_data = Order.objects.values('status').annotate(count=Count('id'))
    status_labels = [s['status'] for s in order_status_data]
    status_counts = [s['count'] for s in order_status_data]

    # --- ANALYTICS DATA ---
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    # 1. User Logins Analytics
    daily_logins = UserLoginHistory.objects.filter(timestamp__gte=thirty_days_ago) \
        .annotate(day=TruncDay('timestamp')) \
        .values('day') \
        .annotate(count=Count('id')) \
        .order_by('day')
        
    login_trend = {}
    for i in range(30, -1, -1):
        date_str = (timezone.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        login_trend[date_str] = 0
        
    for item in daily_logins:
        d_str = item['day'].strftime('%Y-%m-%d')
        if d_str in login_trend:
            login_trend[d_str] = item['count']
            
    login_labels = list(login_trend.keys())
    login_counts = list(login_trend.values())
    
    # KPI Logins Today
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    logins_today = UserLoginHistory.objects.filter(timestamp__date=today).count()
    logins_yesterday = UserLoginHistory.objects.filter(timestamp__date=yesterday).count()
    
    if logins_yesterday > 0:
        login_growth = round(((logins_today - logins_yesterday) / logins_yesterday) * 100, 1)
    else:
        login_growth = None
        
    recent_logins = UserLoginHistory.objects.all().select_related('user').order_by('-timestamp')[:10]
    
    # 2. Product Performance (Clothes by name & size)
    popular_apparel = OrderItem.objects.exclude(order__status='CANCELLED') \
        .values('product_name', 'size') \
        .annotate(
            total_sold=Sum('quantity'),
            revenue=Sum(F('price') * F('quantity'), output_field=models.DecimalField())
        ) \
        .order_by('-total_sold')
        
    apparel_labels = [f"{item['product_name']} ({item['size']})" for item in popular_apparel[:8]]
    apparel_counts = [item['total_sold'] for item in popular_apparel[:8]]
    
    best_selling_variant = popular_apparel[0] if popular_apparel else None
    
    # 3. Top Buyers
    top_buyers_items = OrderItem.objects.exclude(order__status='CANCELLED') \
        .values('order__user__username', 'order__user__email') \
        .annotate(
            order_count=Count('order_id', distinct=True),
            total_units=Sum('quantity'),
            total_spent=Sum(F('price') * F('quantity'), output_field=models.DecimalField())
        ) \
        .order_by('-total_spent')
        
    buyer_labels = [item['order__user__username'] for item in top_buyers_items[:8]]
    buyer_spent = [float(item['total_spent']) for item in top_buyers_items[:8]]
    
    top_buyer = top_buyers_items[0] if top_buyers_items else None
    
    # AOV and Total Units Sold
    aov_dict = Order.objects.exclude(status='CANCELLED').aggregate(avg=Avg('total_amount'))
    avg_order_value = aov_dict['avg'] if aov_dict['avg'] is not None else 0.00
    
    units_sold_dict = OrderItem.objects.exclude(order__status='CANCELLED').aggregate(total=Sum('quantity'))
    total_units_sold = units_sold_dict['total'] if units_sold_dict['total'] is not None else 0

    if DashboardWidget.objects.count() == 0:
        _seed_default_widgets()

    widgets = DashboardWidget.objects.all().order_by('-is_pinned', 'position', 'id')
    total_inventory = Product.objects.aggregate(total=Sum('stock'))['total'] or 0

    widget_list = []
    widgets_json_data = []
    for w in widgets:
        val = ""
        if w.widget_type == 'CARD':
            if w.value_override:
                val = w.value_override
            else:
                if w.key == 'revenue':
                    val = f"${total_revenue:.2f}"
                elif w.key == 'orders':
                    val = str(total_orders)
                elif w.key == 'products':
                    val = str(total_products)
                elif w.key == 'clients':
                    val = str(total_customers)
                elif w.key == 'inventory':
                    val = f"{total_inventory} units"
                elif w.key == 'sales':
                    val = f"{total_units_sold} sold"
                elif w.key == 'statistics':
                    val = f"${avg_order_value:.2f}"
                else:
                    val = "0"
        w.dynamic_value = val
        w.style_string = f"background: {w.bg_color} !important; border-color: {w.border_color} !important; color: {w.text_color} !important; border-radius: 16px; min-height: 140px;"
        w.text_style_string = f"color: {w.text_color} !important;"
        widget_list.append(w)
        
        widgets_json_data.append({
            'key': w.key,
            'title': w.title,
            'widget_type': w.widget_type,
            'chart_type': w.chart_type or None,
            'value_override': w.value_override or None,
            'subtitle': w.subtitle or None,
            'icon': w.icon,
            'text_color': w.text_color,
            'bg_color': w.bg_color,
            'border_color': w.border_color,
            'is_visible': w.is_visible,
            'is_pinned': w.is_pinned,
            'custom_html': w.custom_html or None,
            'custom_description': w.custom_description or None,
            'colors_json': w.colors_json,
            'legend_visible': w.legend_visible,
            'labels_json': w.labels_json or None,
            'refresh_interval': w.refresh_interval,
            'dynamic_value': w.dynamic_value,
        })

    return {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'category_labels': category_labels,
        'category_counts': category_counts,
        'status_labels': status_labels,
        'status_counts': status_counts,
        
        # Analytics context
        'login_labels': login_labels,
        'login_counts': login_counts,
        'logins_today': logins_today,
        'logins_yesterday': logins_yesterday,
        'login_growth': login_growth,
        'recent_logins': recent_logins,
        'popular_apparel': popular_apparel,
        'apparel_labels': apparel_labels,
        'apparel_counts': apparel_counts,
        'best_selling_variant': best_selling_variant,
        'top_buyers': top_buyers_items,
        'buyer_labels': buyer_labels,
        'buyer_spent': buyer_spent,
        'top_buyer': top_buyer,
        'avg_order_value': avg_order_value,
        'total_units_sold': total_units_sold,
        
        # Dynamic widgets
        'widgets': widget_list,
        'widgets_json_data': widgets_json_data,
    }

@staff_member_required
def dashboard_home(request):
    context = _get_dashboard_context()
    return render(request, 'dashboard/dashboard.html', context)

@staff_member_required
@transaction.atomic
def save_dashboard_layout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            widgets_data = data.get('widgets', [])
            updated_keys = []
            
            for index, w_data in enumerate(widgets_data):
                key = w_data.get('key')
                if not key:
                    continue
                
                widget, created = DashboardWidget.objects.get_or_create(key=key)
                widget.title = w_data.get('title', widget.title)
                widget.widget_type = w_data.get('widget_type', widget.widget_type)
                widget.chart_type = w_data.get('chart_type', widget.chart_type)
                widget.value_override = w_data.get('value_override')
                widget.subtitle = w_data.get('subtitle', widget.subtitle)
                widget.icon = w_data.get('icon', widget.icon)
                
                widget.text_color = w_data.get('text_color', widget.text_color)
                widget.bg_color = w_data.get('bg_color', widget.bg_color)
                widget.border_color = w_data.get('border_color', widget.border_color)
                
                widget.is_visible = w_data.get('is_visible', True)
                widget.is_pinned = w_data.get('is_pinned', False)
                widget.position = index
                
                widget.custom_html = w_data.get('custom_html', widget.custom_html)
                widget.custom_description = w_data.get('custom_description', widget.custom_description)
                
                widget.colors_json = w_data.get('colors_json', widget.colors_json)
                widget.legend_visible = w_data.get('legend_visible', widget.legend_visible)
                widget.labels_json = w_data.get('labels_json', widget.labels_json)
                widget.refresh_interval = w_data.get('refresh_interval', widget.refresh_interval)
                
                widget.save()
                updated_keys.append(key)
            
            # Exclude deleted widgets
            DashboardWidget.objects.exclude(key__in=updated_keys).delete()
            
            return JsonResponse({'status': 'success', 'message': 'Layout saved.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method.'}, status=405)

@staff_member_required
def reset_dashboard_layout(request):
    DashboardWidget.objects.all().delete()
    messages.success(request, "Dashboard layout reset successfully.")
    return redirect('dashboard:home')

# --- PRODUCT MANAGEMENT ---
@staff_member_required
def manage_products(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'dashboard/products.html', {'products': products})

@staff_member_required
@transaction.atomic
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            
            # Handle multiple uploaded gallery images
            gallery_images = request.FILES.getlist('gallery_images')
            for img in gallery_images:
                ProductImage.objects.create(product=product, image=img)
                
            messages.success(request, f"Product '{product.name}' added successfully.")
            return redirect('dashboard:manage_products')
    else:
        form = ProductForm()
    return render(request, 'dashboard/product_form.html', {'form': form, 'title': 'Add Product'})

@staff_member_required
@transaction.atomic
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            
            # Add new gallery images if uploaded
            gallery_images = request.FILES.getlist('gallery_images')
            for img in gallery_images:
                ProductImage.objects.create(product=product, image=img)
                
            messages.success(request, f"Product '{product.name}' updated successfully.")
            return redirect('dashboard:manage_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/product_form.html', {'form': form, 'product': product, 'title': 'Edit Product'})

@staff_member_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    name = product.name
    product.delete()
    messages.success(request, f"Product '{name}' deleted successfully.")
    return redirect('dashboard:manage_products')

# --- CATEGORY MANAGEMENT ---
@staff_member_required
def manage_categories(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/categories.html', {'categories': categories})

@staff_member_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"Category '{category.name}' created.")
            return redirect('dashboard:manage_categories')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/category_form.html', {'form': form, 'title': 'Add Category'})

@staff_member_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"Category '{category.name}' updated.")
            return redirect('dashboard:manage_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/category_form.html', {'form': form, 'category': category, 'title': 'Edit Category'})

@staff_member_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    name = category.name
    category.delete()
    messages.success(request, f"Category '{name}' deleted.")
    return redirect('dashboard:manage_categories')

# --- ORDER MANAGEMENT ---
@staff_member_required
def manage_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    
    # Search and Filter
    query = request.GET.get('q')
    status = request.GET.get('status')
    
    if query:
        orders = orders.filter(id__icontains=query) | orders.filter(full_name__icontains=query)
    if status:
        orders = orders.filter(status=status)
        
    return render(request, 'dashboard/orders.html', {'orders': orders, 'query': query, 'selected_status': status})

@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        order.status = status
        order.save()
        messages.success(request, f"Order #{order.id} status updated to {order.get_status_display()}.")
    return redirect('dashboard:manage_orders')

@staff_member_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, f"Order #{order_id} deleted successfully.")
    return redirect('dashboard:manage_orders')

# --- CUSTOMER MANAGEMENT ---
@staff_member_required
def manage_customers(request):
    customers = User.objects.filter(is_staff=False).order_by('-date_joined')
    return render(request, 'dashboard/customers.html', {'customers': customers})

@staff_member_required
def toggle_customer_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    status = "unblocked" if user.is_active else "blocked"
    messages.success(request, f"Customer '{user.username}' has been {status}.")
    return redirect('dashboard:manage_customers')

@staff_member_required
def delete_customer(request, user_id):
    user = get_object_or_404(User, id=user_id)
    username = user.username
    user.delete()
    messages.success(request, f"Customer '{username}' has been deleted.")
    return redirect('dashboard:manage_customers')

# --- REVIEW MANAGEMENT ---
@staff_member_required
def manage_reviews(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'dashboard/reviews.html', {'reviews': reviews})

@staff_member_required
def approve_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.approved = True
    review.save()
    messages.success(request, "Review has been approved.")
    return redirect('dashboard:manage_reviews')

@staff_member_required
def reject_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.approved = False
    review.save()
    messages.success(request, "Review approval has been revoked/rejected.")
    return redirect('dashboard:manage_reviews')

@staff_member_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    messages.success(request, "Review has been deleted.")
    return redirect('dashboard:manage_reviews')

# --- CONTACT MESSAGES ---
@staff_member_required
def manage_contacts(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'dashboard/contacts.html', {'messages_list': messages_list})

@staff_member_required
def delete_contact(request, message_id):
    msg = get_object_or_404(ContactMessage, id=message_id)
    msg.delete()
    messages.success(request, "Contact message deleted.")
    return redirect('dashboard:manage_contacts')

# --- SETTINGS MANAGEMENT ---
@staff_member_required
def manage_settings(request):
    settings_obj = Settings.get_settings()
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Store settings updated successfully.")
            return redirect('dashboard:manage_settings')
    else:
        form = SettingsForm(instance=settings_obj)
    return render(request, 'dashboard/settings.html', {'form': form})


@staff_member_required
def analytics_dashboard(request):
    context = _get_dashboard_context()
    return render(request, 'dashboard/analytics.html', context)

