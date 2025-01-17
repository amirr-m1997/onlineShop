from django import forms
from .models import Order, Size, Color


class CartEditForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, label='تعداد')
    size = forms.ChoiceField(choices=[(size.id, size.name) for size in Size.objects.all()], label='سایز')
    color = forms.ChoiceField(choices=[(color.id, color.name) for color in Color.objects.all()], label='رنگ')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'phone']
