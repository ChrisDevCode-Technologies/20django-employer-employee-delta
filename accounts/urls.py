from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# app_name = 'accounts'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.profile, name='profile'),
]