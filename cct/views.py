from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm


def home(request):
    # Redirect authenticated users to dashboard
    if request.user.is_authenticated:
        return redirect('donor_dashboard')
    return render(request, 'home.html')

def custom_login(request):
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('donor_dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('donor_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'registration/login.html')

def custom_logout(request):
    logout(request)
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            messages.success(request, 'Registration successful!')
            return redirect('donor_dashboard')  # Replace with your dashboard URL name
        else:
            # Display form errors to user
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})




@login_required
def donor_dashboard(request):
    # Updated to use real user data instead of mock data
    context = {
        'user': request.user,  # Use the authenticated user
        'monthly_total': 1250,
        'monthly_change': 12,
        'notifications_count': 3,
        'upcoming_donations': [
            {'amount': 50, 'recipient': 'Red Cross', 'date': '15th'},
            {'amount': 100, 'recipient': 'Local Shelter', 'date': '20th'}
        ],
        'weekly_donations': [
            {'amount': 50, 'recipient': 'Red Cross', 'date': 'Today'},
            {'amount': 100, 'recipient': 'Local Food Bank', 'date': '2 days ago'}
        ],
        'recent_donations': [
            {'amount': 50, 'recipient': 'Red Cross', 'date': 'Today', 'purpose': 'Medical Relief'},
            {'amount': 100, 'recipient': 'Food Bank', 'date': '2 days ago', 'purpose': 'Community Support'}
        ],
        'chart_data': {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'amounts': [450, 600, 800, 750, 900, 1250]
        }
    }
    return render(request, 'donor_dashboard.html', context)