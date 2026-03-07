from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Incident
from apps.incidents.models import Notification

@receiver(post_save, sender=Incident)
def notify_supervisor(sender, instance, created, **kwargs):
    if created:
        supervisor = instance.reported_by.supervisor
        if supervisor:
            Notification.objects.create(
                recipient=supervisor,
                title="New Incident Reported",
                message=f"{instance.reported_by.username} reported an incident: {instance.title}"
            )