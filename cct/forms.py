from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)
    birth_date = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username', 
            'email', 
            'password1', 
            'password2',
            'first_name',
            'last_name',
            'phone',
        ]