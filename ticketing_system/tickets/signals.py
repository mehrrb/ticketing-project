from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket, Notification
from users.models import Users

@receiver(post_save, sender=Ticket)
def create_ticket_notification(sender, instance, created, **kwargs):
    if created:
        for admin in Users.objects.filter(is_superuser=True):
            Notification.objects.create(
                user=admin,
                ticket=instance,
                notification_type='ticket_assigned',
                message=f'New ticket created: {instance.title}'
            )
    elif instance.reply and instance.reply != instance._original_reply:
        Notification.objects.create(
            user=instance.user,
            ticket=instance,
            notification_type='ticket_reply',
            message='Your ticket has received a reply'
        ) 