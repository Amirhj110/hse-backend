import uuid
from django.db import models
from django.conf import settings


class IncidentType(models.TextChoices):
    NEAR_MISS = "NEAR_MISS", "Near Miss"
    UNSAFE_ACT = "UNSAFE_ACT", "Unsafe Act"
    UNSAFE_CONDITION = "UNSAFE_CONDITION", "Unsafe Condition"
    ENVIRONMENTAL = "ENVIRONMENTAL", "Environmental"

class IncidentSeverity(models.TextChoices):
    LOW = "LOW", "Low"
    MEDIUM = "MEDIUM", "Medium"
    HIGH = "HIGH", "High"
    CRITICAL = "CRITICAL", "Critical"

class IncidentStatus(models.TextChoices):
    REPORTED = "REPORTED", "Reported"
    UNDER_INVESTIGATION = "UNDER_INVESTIGATION", "Under Investigation"
    ACTION_TAKEN = "ACTION_TAKEN", "Action Taken"
    CLOSED = "CLOSED", "Closed"

class Incident(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    incident_type = models.CharField(max_length=30, choices=IncidentType.choices, default=None)
    severity = models.CharField(max_length=20, choices=IncidentSeverity.choices)
    status = models.CharField(max_length=30, choices=IncidentStatus.choices, default=IncidentStatus.REPORTED)

    # Reporting & Assignment
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reported_incidents",
        limit_choices_to={"role": "HSE_OFFICER"}
    )
    assigned_supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supervised_incidents",
        limit_choices_to={"role": "HSE_SUPERVISOR"}
    )
    responsible_party = models.CharField(max_length=255, blank=True, help_text="Field supervisor or team responsible for action")

    location = models.CharField(max_length=255, blank=True)  # optional GPS/text
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.status})"

class IncidentPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="incident_photos/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.incident.title}"

class CorrectiveAction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="actions")
    description = models.TextField()
    responsible_party = models.CharField(max_length=255, blank=True)  # can be field supervisor or officer
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[("PENDING","Pending"), ("COMPLETED","Completed")], default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Action for {self.incident.title}"
    
class Notification(models.Model):
    NOTIF_TYPES = [
        ("INFO", "Info"),
        ("SUGGESTION", "Suggestion"),
        ("WARNING", "Warning"),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    incident = models.ForeignKey(Incident, null=True, blank=True, on_delete=models.CASCADE)
    message = models.TextField()
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPES, default="INFO")
    read_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)