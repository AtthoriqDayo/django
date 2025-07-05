from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('articles/', views.manage_articles_view, name='manage_articles'),
    path('articles/create/', views.create_article_view, name='create_article'),
    path('articles/update/<int:pk>/', views.update_article_view, name='update_article'),
    path('articles/delete/<int:pk>/', views.delete_article_view, name='delete_article'),
    path('import-news/', views.import_news_view, name='import_news'),
    path('save-news/', views.save_news_view, name='save_news'),
    path('users/', views.manage_users_view, name='manage_users'),
    path('users/edit/<int:pk>/', views.edit_user_view, name='edit_user'),
    path('users/delete/<int:pk>/', views.delete_user_view, name='delete_user'),
]