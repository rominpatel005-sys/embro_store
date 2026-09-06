from django import forms
from products.models import Product, Category
from .models import Settings

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'discount_price', 'category', 'brand', 'stock', 'sizes', 'colors', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'gender']

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['store_name', 'logo', 'contact_email', 'contact_phone', 'address', 'facebook_url', 'instagram_url', 'twitter_url']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
