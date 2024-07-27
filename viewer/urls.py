from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView, create_payment, execute_payment, cancel_payment, success_payment, download_image
from django.contrib import admin


urlpatterns = [
    path('', views.home, name='home'),
    path('albums/', views.album_list, name='albums'),
    path('albums/<int:album_id>/', views.album_detail, name='album_detail'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('About/', views.About, name='About'),
    path('Contact/', views.Contact, name='Contact'),
    path('Blog/', views.Blog, name='Blog'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('payment/create/', create_payment, name='create_payment'),
    path('payment/execute/', execute_payment, name='execute_payment'),
    path('payment/cancel/', cancel_payment, name='cancel_payment'),
    path('payment/success/', success_payment, name='success_payment'),
    path('download-image/<int:post_id>/', download_image, name='download_image'),
]

