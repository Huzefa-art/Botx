from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator

email_regex = RegexValidator(regex=r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', message="Please enter valid Email address.")
mobile_regex = RegexValidator(regex=r'^(\+\d{1,3})?\d{10}$',message='Enter a valid 10-digit mobile number +91 9999999999')

class UserManager(BaseUserManager):
   
    def create_user(self, email, password=None, password2=None ,**extra_fields):
        
        if not email:
            raise ValueError('Email for user must be set.')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)



# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=50, unique=True, validators=[email_regex])
    username = models.CharField(verbose_name="username", max_length=50)
    # phone = models.CharField(verbose_name="phone", validators=[mobile_regex])

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    object = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email