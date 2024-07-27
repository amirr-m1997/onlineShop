from django.urls import path, include
from onlineShop import settings
from . import views

urlpatterns = [
    path('', views.cart_summery, name='cart_summery'),
    path('add/', views.cart_add, name='cart_add'),
    path('delete/', views.cart_delete, name='cart_delete'),
    # path('update/', views.cart_update, name='cart_update'),
    path('cart/edit/<int:product_id>/', views.cart_edit, name='cart_edit'),
    path('cart/update/', views.cart_update, name='cart_update'),
    ]
