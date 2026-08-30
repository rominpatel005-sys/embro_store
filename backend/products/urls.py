from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('api/search/', views.ajax_search, name='ajax_search'),
    path('custom/', views.custom_design, name='custom_design'),
]
