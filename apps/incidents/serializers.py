from rest_framework import serializers
from .models import Incident, IncidentPhoto, CorrectiveAction, Notification
from apps.users.models import User

class IncidentPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentPhoto
        fields = ["id", "image", "uploaded_at"]

class CorrectiveActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorrectiveAction
        fields = ["id", "description", "responsible_party", "due_date", "status", "created_at", "updated_at"]

class IncidentSerializer(serializers.ModelSerializer):
    photos = IncidentPhotoSerializer(many=True, read_only=True)
    actions = CorrectiveActionSerializer(many=True, read_only=True)
    reported_by = serializers.StringRelatedField(read_only=True)
    assigned_supervisor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Incident
        fields = [
            "id",
            "title",
            "description",
            "incident_type",
            "severity",
            "status",
            "reported_by",
            "assigned_supervisor",
            "responsible_party",
            "location",
            "photos",
            "actions",
            "created_at",
            "updated_at",
        ]

class IncidentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = [
            "title",
            "description",
            "incident_type",
            "severity",
            "status",
            "assigned_supervisor",
            "responsible_party",
            "location",
        ]

    def create(self, validated_data):
        validated_data["reported_by"] = self.context["request"].user
        return super().create(validated_data)
    
class NotificationSerializer(serializers.ModelSerializer):
    Incident = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'incident', 'message', 'notif_type', 'read_status', 'created_at']
    

    