from django.contrib import admin
from .models import Category, Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('gender',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount_price', 'stock', 'rating', 'created_at')
    list_filter = ('category', 'category__gender', 'created_at')
    search_fields = ('name', 'description', 'brand')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
