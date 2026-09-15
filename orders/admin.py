from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price', 'quantity', 'size', 'color', 'custom_design_preview')

    def custom_design_preview(self, obj):
        if obj.custom_image_url:
            return format_html(
                '<a href="{0}" target="_blank" style="display:inline-block; margin-right:8px;">'
                '<img src="{0}" style="max-height: 55px; max-width: 55px; object-fit: contain; border: 1px solid #ddd; border-radius: 4px;" />'
                '</a><br><a href="{0}" download style="font-weight:bold;">Download File</a>',
                obj.custom_image_url
            )
        return "-"
    custom_design_preview.short_description = "Custom Design"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'mobile', 'total_amount', 'status', 'cancel_reason', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email', 'mobile', 'id', 'cancel_reason')
    list_editable = ('status',)
    inlines = [OrderItemInline]
