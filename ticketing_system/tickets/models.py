from django.db import models
from users.models import Users

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('ticket_reply', 'Ticket Reply'),
        ('status_change', 'Status Change'),
        ('ticket_assigned', 'Ticket Assigned'),
    ]

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='users', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    is_read_by_admin = models.BooleanField(default=False)
    reply = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
