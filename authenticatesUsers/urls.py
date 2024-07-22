from django.urls import path, include
from onlineShop import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
    # path('login/', login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_page, name='login'),    # Login page
    path('register/', views.register_page, name='register'),  # Registration page

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

