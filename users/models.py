from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    country = models.CharField(max_length=100)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_user_active = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    email = models.CharField(max_length=200, unique=True)
