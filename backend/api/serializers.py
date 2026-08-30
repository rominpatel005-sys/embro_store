from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from accounts.models import UserProfile
from cart.models import Cart, CartItem
from contacts.models import ContactMessage, Newsletter
from dashboard.models import Settings
from orders.models import Order, OrderItem
from payments.models import Payment
from products.models import Category, Product, ProductImage
from reviews.models import Review
from wishlist.models import Wishlist


class RelativeImageField(serializers.ImageField):
    def to_representation(self, value):
        return value.url if value else None


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    mobile = serializers.CharField(write_only=True, max_length=15)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'mobile', 'password')
        extra_kwargs = {'email': {'required': True}, 'first_name': {'required': True}}

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('An account with this email already exists.')
        return value.lower()

    def create(self, validated_data):
        mobile = validated_data.pop('mobile')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        user.profile.mobile = mobile
        user.profile.save(update_fields=['mobile'])
        return user


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name', allow_blank=True)
    last_name = serializers.CharField(source='user.last_name', allow_blank=True)
    is_staff = serializers.BooleanField(source='user.is_staff', read_only=True)
    profile_image = RelativeImageField(required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'mobile',
                  'address', 'state', 'city', 'pincode', 'profile_image', 'email_verified')
        read_only_fields = ('email_verified',)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        for field in ('email', 'first_name', 'last_name'):
            if field in user_data:
                setattr(instance.user, field, user_data[field])
        instance.user.save()
        return super().update(instance, validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'gender')
        read_only_fields = ('slug',)


class ProductImageSerializer(serializers.ModelSerializer):
    image = RelativeImageField()

    class Meta:
        model = ProductImage
        fields = ('id', 'image')

class ProductSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)
    gallery = ProductImageSerializer(many=True, read_only=True)
    current_price = serializers.DecimalField(source='get_price', max_digits=10, decimal_places=2, read_only=True)
    sizes_list = serializers.SerializerMethodField()
    colors_list = serializers.SerializerMethodField()
    image = RelativeImageField(required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'description', 'price', 'discount_price', 'current_price',
                  'category', 'category_detail', 'brand', 'stock', 'rating', 'image', 'gallery',
                  'sizes', 'colors', 'sizes_list', 'colors_list', 'created_at', 'updated_at')
        read_only_fields = ('slug', 'rating', 'created_at', 'updated_at')

    def get_sizes_list(self, obj):
        return [value.strip() for value in obj.sizes.split(',') if value.strip()]

    def get_colors_list(self, obj):
        return [value.strip() for value in obj.colors.split(',') if value.strip()]

    def validate(self, attrs):
        price = attrs.get('price', getattr(self.instance, 'price', None))
        discount = attrs.get('discount_price', getattr(self.instance, 'discount_price', None))
        stock = attrs.get('stock', getattr(self.instance, 'stock', 0))
        if price is not None and price <= 0:
            raise serializers.ValidationError({'price': 'Price must be positive.'})
        if discount is not None and price is not None and discount >= price:
            raise serializers.ValidationError({'discount_price': 'Discount price must be below price.'})
        if stock < 0:
            raise serializers.ValidationError({'stock': 'Stock cannot be negative.'})
        return attrs


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    profile_image = RelativeImageField(required=False, allow_null=True)

    class Meta:
        model = Review
        fields = ('id', 'product', 'product_name', 'username', 'rating', 'comment',
                  'profile_image', 'approved', 'created_at')
        read_only_fields = ('approved', 'created_at')


class CartItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    subtotal = serializers.DecimalField(source='get_subtotal', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_detail', 'quantity', 'size', 'color', 'subtotal')


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(source='get_total_price', max_digits=10, decimal_places=2, read_only=True)
    total_items = serializers.IntegerField(source='get_total_items', read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'items', 'total_price', 'total_items', 'updated_at')


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(source='get_subtotal', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'price', 'quantity', 'size', 'color', 'subtotal')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'payment_method', 'transaction_id', 'amount', 'status', 'created_at')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)
    customer = serializers.CharField(source='user.username', read_only=True)
    cancellable = serializers.BooleanField(source='is_cancellable', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'customer', 'full_name', 'mobile', 'email', 'address', 'state', 'city',
                  'pincode', 'total_amount', 'status', 'cancellable', 'items', 'payment',
                  'created_at', 'updated_at')
        read_only_fields = ('total_amount', 'status', 'created_at', 'updated_at')


class CheckoutSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150)
    mobile = serializers.CharField(max_length=15)
    email = serializers.EmailField()
    address = serializers.CharField()
    state = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=100)
    pincode = serializers.CharField(max_length=10)
    payment_method = serializers.ChoiceField(choices=('COD', 'UPI', 'CREDIT_CARD', 'DEBIT_CARD', 'NET_BANKING'))


class WishlistSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = Wishlist
        fields = ('id', 'product', 'product_detail', 'created_at')


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'
        read_only_fields = ('created_at',)


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ('email', 'subscribed_at')
        read_only_fields = ('subscribed_at',)


class SettingsSerializer(serializers.ModelSerializer):
    logo = RelativeImageField(required=False, allow_null=True)

    class Meta:
        model = Settings
        fields = '__all__'
