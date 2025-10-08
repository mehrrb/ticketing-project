from django.contrib import admin
from .models import Ticket, Category, Notification

admin.site.register(Ticket)
admin.site.register(Category)
admin.site.register(Notification)
