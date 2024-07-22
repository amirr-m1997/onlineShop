from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class RegisterForm(forms.Form):
    first_name = forms.CharField(
        label='نام',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام را وارد کنید', 'required': 'required'})

    )
    last_name = forms.CharField(
        label='نام خانوادگی',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی را وارد کنید', 'required': 'required'})
    )
    username = forms.CharField(
        label='ایمیل یا نام کاربری',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری را وارد کنید', 'required': 'required'})
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور را وارد کنید', 'required': 'required'})
    )
