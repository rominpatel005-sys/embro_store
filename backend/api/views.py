from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Avg, Count, F, Q, Sum
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from cart.models import Cart, CartItem
from contacts.models import ContactMessage, Newsletter
from dashboard.models import Settings
from orders.models import ORDER_STATUS_CHOICES, Order, OrderItem
from payments.models import Payment
from products.models import Category, Product
from reviews.models import Review
from wishlist.models import Wishlist

from .permissions import IsStaff, IsStaffOrReadOnly
from .serializers import (CartItemSerializer, CartSerializer, CategorySerializer,
                          CheckoutSerializer, ContactSerializer, NewsletterSerializer,
                          OrderSerializer, ProductSerializer, ProfileSerializer,
                          RegisterSerializer, ReviewSerializer, SettingsSerializer,
                          WishlistSerializer)


@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    return Response({'status': 'ok'})


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(pk=response.data['id'])
        refresh = RefreshToken.for_user(user)
        response.data['access'] = str(refresh.access_token)
        response.data['refresh'] = str(refresh)
        return response


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'brand', 'category__name']
    ordering_fields = ['price', 'rating', 'created_at', 'name']

    def get_queryset(self):
        queryset = Product.objects.select_related('category').prefetch_related('gallery')
        params = self.request.query_params
        if params.get('gender'):
            queryset = queryset.filter(category__gender=params['gender'].upper())
        if params.get('category'):
            queryset = queryset.filter(category__slug=params['category'])
        if params.get('brand'):
            queryset = queryset.filter(brand__iexact=params['brand'])
        if params.get('min_price'):
            queryset = queryset.filter(price__gte=params['min_price'])
        if params.get('max_price'):
            queryset = queryset.filter(price__lte=params['max_price'])
        return queryset.order_by('-created_at')

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def related(self, request, slug=None):
        product = self.get_object()
        queryset = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]
        return Response(self.get_serializer(queryset, many=True).data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('gender', 'name')
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Review.objects.select_related('user', 'product')
        if not self.request.user.is_authenticated or not self.request.user.is_staff:
            queryset = queryset.filter(approved=True)
        if self.request.query_params.get('product'):
            queryset = queryset.filter(product_id=self.request.query_params['product'])
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, approved=False)

    def perform_update(self, serializer):
        if not self.request.user.is_staff and serializer.instance.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied()
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_staff and instance.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied()
        instance.delete()


def user_cart(user):
    cart = Cart.objects.filter(user=user).first()
    return cart or Cart.objects.create(user=user)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(CartSerializer(user_cart(request.user), context={'request': request}).data)

    @transaction.atomic
    def post(self, request):
        cart = user_cart(request.user)
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = get_object_or_404(Product, pk=serializer.validated_data['product'].pk)
        quantity = serializer.validated_data['quantity']
        size = serializer.validated_data['size']
        color = serializer.validated_data['color']
        if quantity < 1:
            return Response({'quantity': 'Quantity must be positive.'}, status=400)
        if size not in [x.strip() for x in product.sizes.split(',')]:
            return Response({'size': 'Invalid product size.'}, status=400)
        if color not in [x.strip() for x in product.colors.split(',')]:
            return Response({'color': 'Invalid product color.'}, status=400)
        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, size=size, color=color, defaults={'quantity': quantity}
        )
        final_quantity = quantity if created else item.quantity + quantity
        if final_quantity > product.stock:
            if created:
                item.delete()
            return Response({'quantity': 'Requested quantity exceeds stock.'}, status=400)
        item.quantity = final_quantity
        item.save(update_fields=['quantity'])
        return Response(CartSerializer(cart, context={'request': request}).data, status=201)


class CartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        try:
            quantity = int(request.data.get('quantity'))
        except (TypeError, ValueError):
            return Response({'quantity': 'A valid quantity is required.'}, status=400)
        if quantity < 1 or quantity > item.product.stock:
            return Response({'quantity': 'Quantity must be between 1 and available stock.'}, status=400)
        item.quantity = quantity
        item.save(update_fields=['quantity'])
        return Response(CartSerializer(item.cart, context={'request': request}).data)

    def delete(self, request, pk):
        item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        cart = item.cart
        item.delete()
        return Response(CartSerializer(cart, context={'request': request}).data)


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = Cart.objects.filter(user=request.user).prefetch_related('items__product').first()
        if not cart or not cart.items.exists():
            return Response({'detail': 'Cart is empty.'}, status=400)
        products = {p.pk: p for p in Product.objects.select_for_update().filter(
            pk__in=cart.items.values_list('product_id', flat=True)
        )}
        for item in cart.items.all():
            if products[item.product_id].stock < item.quantity:
                return Response({'detail': f'Insufficient stock for {item.product.name}.'}, status=409)
        data = serializer.validated_data.copy()
        payment_method = data.pop('payment_method')
        order = Order.objects.create(user=request.user, total_amount=cart.get_total_price, **data)
        for item in cart.items.all():
            product = products[item.product_id]
            product.stock = F('stock') - item.quantity
            product.save(update_fields=['stock'])
            OrderItem.objects.create(order=order, product=product, product_name=product.name,
                                     price=product.get_price, quantity=item.quantity,
                                     size=item.size, color=item.color)
        Payment.objects.create(order=order, payment_method=payment_method,
                               amount=order.total_amount, status='PENDING')
        cart.items.all().delete()
        return Response(OrderSerializer(order, context={'request': request}).data, status=201)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Order.objects.prefetch_related('items').select_related('payment', 'user')
        return queryset if self.request.user.is_staff else queryset.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def cancel(self, request, pk=None):
        order = self.get_object()
        order = Order.objects.select_for_update().get(pk=order.pk)
        if not order.is_cancellable:
            return Response({'detail': 'This order cannot be cancelled.'}, status=409)
        order.status = 'CANCELLED'
        order.save(update_fields=['status', 'updated_at'])
        for item in order.items.select_related('product'):
            if item.product_id:
                Product.objects.filter(pk=item.product_id).update(stock=F('stock') + item.quantity)
        return Response(OrderSerializer(order, context={'request': request}).data)


class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('product__category')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContactView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]


class NewsletterView(generics.CreateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [AllowAny]


class SettingsView(generics.RetrieveUpdateAPIView):
    serializer_class = SettingsSerializer

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [IsStaff()]

    def get_object(self):
        return Settings.get_settings()


class AdminOverview(APIView):
    permission_classes = [IsStaff]

    def get(self, request):
        paid_revenue = Order.objects.filter(payment__status='PAID').aggregate(value=Sum('total_amount'))['value'] or 0
        statuses = list(Order.objects.values('status').annotate(count=Count('id')).order_by('status'))
        categories = list(Category.objects.annotate(count=Count('products')).values('name', 'count'))
        return Response({
            'products': Product.objects.count(), 'orders': Order.objects.count(),
            'customers': User.objects.filter(is_staff=False).count(), 'revenue': paid_revenue,
            'low_stock': ProductSerializer(Product.objects.filter(stock__lt=5), many=True, context={'request': request}).data,
            'order_statuses': statuses, 'category_share': categories,
            'recent_orders': OrderSerializer(Order.objects.all()[:10], many=True, context={'request': request}).data,
        })


class AdminOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('user', 'payment').prefetch_related('items')
    serializer_class = OrderSerializer
    permission_classes = [IsStaff]

    @action(detail=True, methods=['post'])
    def status(self, request, pk=None):
        value = request.data.get('status')
        if value not in dict(ORDER_STATUS_CHOICES):
            return Response({'status': 'Invalid order status.'}, status=400)
        order = self.get_object()
        order.status = value
        order.save(update_fields=['status', 'updated_at'])
        return Response(self.get_serializer(order).data)
