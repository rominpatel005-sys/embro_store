from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (AdminOrderViewSet, AdminOverview, CartItemView, CartView,
                    CategoryViewSet, CheckoutView, ContactView, NewsletterView,
                    OrderViewSet, ProductViewSet, ProfileView, RegisterView,
                    ReviewViewSet, SettingsView, WishlistViewSet, health)

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('categories', CategoryViewSet, basename='category')
router.register('reviews', ReviewViewSet, basename='review')
router.register('orders', OrderViewSet, basename='order')
router.register('wishlist', WishlistViewSet, basename='wishlist')
router.register('staff/orders', AdminOrderViewSet, basename='staff-order')

urlpatterns = [
    path('health/', health),
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('auth/me/', ProfileView.as_view()),
    path('cart/', CartView.as_view()),
    path('cart/items/<int:pk>/', CartItemView.as_view()),
    path('checkout/', CheckoutView.as_view()),
    path('contact/', ContactView.as_view()),
    path('newsletter/', NewsletterView.as_view()),
    path('settings/', SettingsView.as_view()),
    path('staff/overview/', AdminOverview.as_view()),
    path('', include(router.urls)),
]
