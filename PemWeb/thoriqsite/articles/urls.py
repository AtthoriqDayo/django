from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.article_list_view, name='list'),
    path('article/<int:pk>/', views.article_detail_view, name='detail'),
]