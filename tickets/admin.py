from django.contrib import admin

from .models import Category, Notification, Ticket

admin.site.register(Ticket)
admin.site.register(Category)
admin.site.register(Notification)
