from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    # Password reset URLs
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset/done/', TemplateView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/<str:token>/', views.PasswordResetConfirmView.as_view(), 
        name='password_reset_confirm'),
    path('password-reset/complete/', TemplateView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    path('dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('add_donation/', views.add_donation, name='add_donation'),
    path('set_reminder/',views.set_reminder,name='set_reminder'),
    path('generate_report/',views.generate_report,name='generate_report'),
    path('donation_history/',views.donation_history,name='donation_history')
]