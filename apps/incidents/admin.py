from django.contrib import admin
from .models import Incident, IncidentPhoto

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ("title", "severity", "status", "reported_by", "created_at")
    readonly_fields = ("created_at", "updated_at")
    
    def save_model(self, request, obj, form, change):
        # Automatically assign the logged-in user if reported_by is empty
        if not obj.reported_by:
            obj.reported_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(IncidentPhoto)
class IncidentPhotoAdmin(admin.ModelAdmin):
    list_display = ("incident", "uploaded_at")