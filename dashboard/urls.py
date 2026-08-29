from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard Home
    path('', views.dashboard_home, name='home'),
    path('layout/save/', views.save_dashboard_layout, name='save_dashboard_layout'),
    path('layout/reset/', views.reset_dashboard_layout, name='reset_dashboard_layout'),
    
    # Products
    path('products/', views.manage_products, name='manage_products'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    
    # Categories
    path('categories/', views.manage_categories, name='manage_categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    
    # Orders
    path('orders/', views.manage_orders, name='manage_orders'),
    path('orders/update/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('orders/delete/<int:order_id>/', views.delete_order, name='delete_order'),
    
    # Customers
    path('customers/', views.manage_customers, name='manage_customers'),
    path('customers/toggle/<int:user_id>/', views.toggle_customer_status, name='toggle_customer_status'),
    path('customers/delete/<int:user_id>/', views.delete_customer, name='delete_customer'),
    
    # Reviews
    path('reviews/', views.manage_reviews, name='manage_reviews'),
    path('reviews/approve/<int:review_id>/', views.approve_review, name='approve_review'),
    path('reviews/reject/<int:review_id>/', views.reject_review, name='reject_review'),
    path('reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    
    # Contacts
    path('contacts/', views.manage_contacts, name='manage_contacts'),
    path('contacts/delete/<int:message_id>/', views.delete_contact, name='delete_contact'),
    
    # Settings
    path('settings/', views.manage_settings, name='manage_settings'),
    
    # Analytics
    path('analytics/', views.analytics_dashboard, name='analytics'),
]
