from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password = None,role=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if username is None:
            username = email.split('@')[0]
        if role not in ['admin', 'buyer']:
            raise ValueError("Inalid Role")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            role=role,
            **extra_fields
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        user = self.create_user(email, username=username, password=password, role='admin')
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin','Admin'),
        ('buyer','Buyer'),
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length= 10, choices=ROLE_CHOICES, default='buyer')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    username = models.CharField(max_length=255)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','role']

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,object=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
