from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import TemplateView
from django.urls import reverse
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .forms import *
from .models import *
import datetime

def home(request):
    """
    Home page view - displays different content based on authentication status
    """
    context = {
        'user': request.user,
        'is_authenticated': request.user.is_authenticated
    }
    return render(request, 'home.html', context)

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('donor_dashboard')  # Updated redirect
        return render(request, 'registration/register.html', {'form': form})

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('donor_dashboard')  # Redirect to dashboard after login

class CustomLogoutView(LogoutView):
    next_page = 'home'

class PasswordResetRequestView(View):
    def get(self, request):
        form = CustomPasswordResetForm()
        return render(request, 'registration/password_reset_request.html', {'form': form})

    def post(self, request):
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = CustomUser.objects.filter(email__iexact=email, is_active=True)
            for user in users:
                token = PasswordResetToken.create_token(user)
                reset_url = request.build_absolute_uri(
                    reverse('password_reset_confirm', kwargs={'token': token.token})
                )
                subject = "Password Reset Request"
                message = render_to_string('registration/password_reset_email.html', {
                    'user': user,
                    'reset_url': reset_url,
                })
                send_mail(
                    subject,
                    message,
                    None,
                    [user.email],
                    fail_silently=False,
                )
            return redirect('password_reset_done')
        return render(request, 'registration/password_reset_request.html', {'form': form})

class PasswordResetConfirmView(View):
    def get(self, request, token):
        try:
            token_obj = PasswordResetToken.objects.get(token=token)
            if not token_obj.is_valid():
                return render(request, 'registration/password_reset_invalid.html')
            
            form = CustomSetPasswordForm(token_obj.user)
            return render(request, 'registration/password_reset_confirm.html', {
                'form': form,
                'token': token
            })
        except PasswordResetToken.DoesNotExist:
            return render(request, 'registration/password_reset_invalid.html')

    def post(self, request, token):
        try:
            token_obj = PasswordResetToken.objects.get(token=token)
            if not token_obj.is_valid():
                return render(request, 'registration/password_reset_invalid.html')
            
            form = CustomSetPasswordForm(token_obj.user, request.POST)
            if form.is_valid():
                form.save()
                token_obj.delete()
                return redirect('password_reset_complete')
            return render(request, 'registration/password_reset_confirm.html', {
                'form': form,
                'token': token
            })
        except PasswordResetToken.DoesNotExist:
            return render(request, 'registration/password_reset_invalid.html')

@login_required
def donor_dashboard(request):
    context = {
        'user': request.user,
        'last_login': request.user.last_login,
        'date_joined': request.user.date_joined
    }
    return render(request, 'donor_dashboard.html', context)


@login_required
def add_donation(request):
    if request.method == 'GET':
        form = Add_donationForm()
        return render(request, 'add_donation.html', {'form': form})

    if request.method == 'POST':
        form = Add_donationForm(request.POST)
        
        # Debug: Print the raw POST data
        print("🔍 POST data:", request.POST)
        
        


        if form.is_valid():
            # Debug: Print cleaned data
            print("✅ Cleaned Data:", form.cleaned_data)

            # Prepare before saving
            donation = form.save(commit=False)
            donation.user = request.user  # Ensure the user is assigned
            donation.save()

            return redirect('donor_dashboard')
        else:
            # Debug: Print form errors
            print("❌ Form Errors:", form.errors)

        return render(request, 'add_donation.html', {'form': form})


@login_required
def set_reminder(request):
   
    donation_list = Add_Donation.objects.all()
   
    if request.method == 'POST':
       form = ReminderForm(request.POST)

       if form.is_valid():
            reminder = form.save(commit=False)

            reminder.save()
            
            return redirect('donor_dashboard')
    
    else:
        form = ReminderForm()

    return render(request, 'set_reminder.html', {'form': form})


def generate_report(request):
   
    return render(request, 'generate_report.html')

def donation_history(request):
   
    return render(request, 'donation_history.html')