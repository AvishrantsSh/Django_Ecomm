from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from uuid import uuid4
from django.core.validators import RegexValidator
import jsonfield

class CustomUser(AbstractUser):
    reg = RegexValidator(r'^[0-9]*$','Only Numbers are Allowed')
    id = models.UUIDField(primary_key=True, default = uuid4)
    username = models.CharField(max_length=50, unique=False)
    phone = models.CharField(max_length=10, validators=[reg])
    email = models.EmailField(unique=True, blank=False)
    address = jsonfield.JSONField()
    first_name = None
    last_name = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','phone']

# Create your models here.
