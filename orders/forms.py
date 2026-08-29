from django import forms
from .models import Order
from payments.models import PAYMENT_METHOD_CHOICES

class OrderCreateForm(forms.ModelForm):
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect,
        initial='COD'
    )

    class Meta:
        model = Order
        fields = ['full_name', 'email', 'mobile', 'address', 'state', 'city', 'pincode']
