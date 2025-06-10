from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('register/', views.register_view, name='register'),


     # Authentication URLs
    path('accounts/login/', views.custom_login, name='login'),
    path('accounts/logout/', views.custom_logout, name='logout'),

    path('donations/add/', views.donor_dashboard, name='add_donation'),
    path('donations/history/', views.donor_dashboard, name='donation_history'),
    path('reminders/', views.donor_dashboard, name='set_reminder'),
    path('reports/', views.donor_dashboard, name='generate_report'),
]