from django.urls import path, include
from onlineShop import settings
from . import views
urlpatterns = [
    path('', views.go_to_gateway_view, name='go_to_gateway_view'),
    path('callback/', views.callback_gateway_view, name='callback_gateway_view'),
]

