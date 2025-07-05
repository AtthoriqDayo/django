# users/urls.py
from django.urls import path
from . import views

# app_name diperlukan agar reverse() berfungsi dengan baik
app_name = 'users'

urlpatterns = [
    path('guest-login/', views.guest_login_view, name='guest_login'),
    # URL baru untuk dispatch view kita
    path('home/', views.home_dispatch_view, name='home_dispatch'),
     path('profile/', views.profile_view, name='profile'),
]