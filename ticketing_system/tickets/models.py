from django.db import models
from users.models import Users





class Ticket(models.Model):
    
    
    
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    user = models.ForeignKey(Users,on_delete=models.DO_NOTHING)
    is_read_by_admin = models.BooleanField(default=False)
    reply = models.TextField(null=True, blank=True)
    
