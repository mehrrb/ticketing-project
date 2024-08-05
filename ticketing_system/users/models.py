from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Users(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(null=True, blank=True,unique= True)
    username = models.CharField(
        ("username"),
        max_length=150,
        unique=False,
        null=True,
        blank=True
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'username']
    
    
    def __str__(self):
        return self.email