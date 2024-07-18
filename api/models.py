from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from datetime import timedelta
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    api_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    failed_login_attempts = models.IntegerField(default=0)
    last_login_attempt = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def generate_api_key(self):
        self.api_key = uuid.uuid4()
        self.save()

    def get_api_key(self):
        return self.api_key
    
    def get_name(self):
        return self.name

    def login_attempt_failed(self):
        self.failed_login_attempts += 1
        self.last_login_attempt = timezone.now()
        self.save()

    def reset_login_attempts(self):
        self.failed_login_attempts = 0
        self.last_login_attempt = None
        self.save()

    @property
    def is_blocked(self):
        
        return self.failed_login_attempts >= 5 and \
               self.last_login_attempt and \
               timezone.now() < self.last_login_attempt + timezone.timedelta(hours=24)


class RequestLog(models.Model):
    user = models.CharField(max_length=100, null=True, blank=True)
    from_currency = models.CharField(max_length=3)
    to_currency = models.CharField(max_length=3)
    rate = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    browser = models.CharField(max_length=100, null=True, blank=True)
    os = models.CharField(max_length=100, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    isp = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} converted {self.from_currency} to {self.to_currency} at rate {self.rate}"


class Plan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()  # Duration of the plan in days

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    # fields for billing
    last_billed = models.DateTimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def bill_user(self):
        if not self.is_paid and self.is_active():
            self.amount_due = self.calculate_amount_due()
            self.amount_paid = self.amount_due
            self.last_billed = timezone.now()
            self.is_paid = True
            self.save()

    def calculate_amount_due(self):
        return self.plan.price

    def save(self, *args, **kwargs):
        if not self.end_date:
            if not self.start_date:
                self.start_date = timezone.now()
            self.end_date = self.start_date + timezone.timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    def is_active(self):
        return self.end_date >= timezone.now()

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"
