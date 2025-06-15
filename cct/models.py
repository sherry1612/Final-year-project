from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.core.validators import RegexValidator
import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
            
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    # Custom fields
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'"
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        unique=True
    )
    
    # Additional fields
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        null=True,
        blank=True
    )
    
    # Metadata
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'custom_users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.email

class PasswordResetToken(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='password_reset_tokens'
    )
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Password Reset Token'
        verbose_name_plural = 'Password Reset Tokens'
        db_table = 'password_reset_tokens'
        ordering = ['-created_at']
    
    @classmethod
    def create_token(cls, user):
        cls.objects.filter(user=user).delete()
        return cls.objects.create(
            user=user,
            token=get_random_string(64),
            expires_at=timezone.now() + datetime.timedelta(hours=24)
        )
    
    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at
    
    def mark_as_used(self):
        self.is_used = True
        self.save()


class Add_Donation(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=None)
    FullName = models.CharField(max_length=255,default=None,blank=True)
    Donation_date = models.DateTimeField()
    Type_of_Donation = models.CharField(max_length=255,choices=[('Blood','Blood'),('Money','Money'),('Clothes','Clothes'),('Others','Others')])
    Donation_description = models.CharField(max_length=255,default=None,blank=True)
    Quantity = models.DecimalField(max_digits=50,default=255,decimal_places=3,blank=True)
    Purpose = models.CharField(max_length=255,default=None,blank=True)
    payment_method = models.CharField(max_length=255,choices=[('Mobile','Mobile'),('Bank','Bank'),('Cash','Cash')])



class Reminder(models.Model):
    donation = models.ForeignKey(Add_Donation, on_delete=models.CASCADE, related_name='reminders')
    reminder_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

   
    
