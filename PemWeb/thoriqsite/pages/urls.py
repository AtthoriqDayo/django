# pages/urls.py
from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.welcoming_view, name='welcome'),
]