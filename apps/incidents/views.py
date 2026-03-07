from rest_framework import viewsets, permissions
from .models import Incident, IncidentPhoto, CorrectiveAction
from .serializers import IncidentSerializer, IncidentCreateSerializer, IncidentPhotoSerializer, CorrectiveActionSerializer
from .permissions import IsOwnerOrSupervisorOrManager
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Notification
from .serializers import NotificationSerializer

class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSupervisorOrManager]

    def get_serializer_class(self):
        if self.action in ["create"]:
            return IncidentCreateSerializer
        return IncidentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == "HSE_OFFICER":
            return self.queryset.filter(reported_by=user)
        elif user.role == "HSE_SUPERVISOR":
            return self.queryset.filter(assigned_supervisor=user)
        elif user.role == "HSE_MANAGER":
            return self.queryset
        return self.queryset.none()

    @action(detail=True, methods=["post"])
    def upload_photo(self, request, pk=None):
        incident = self.get_object()
        serializer = IncidentPhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(incident=incident)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["incident_type", "severity", "status", "assigned_supervisor"]
    search_fields = ["title", "description", "responsible_party"]
    ordering_fields = ["created_at", "severity"]
    ordering = ["-created_at"]

class CorrectiveActionViewSet(viewsets.ModelViewSet):
    queryset = CorrectiveAction.objects.all()
    serializer_class = CorrectiveActionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "HSE_MANAGER":
            return self.queryset
        elif user.role == "HSE_SUPERVISOR":
            return self.queryset.filter(incident__assigned_supervisor=user)
        elif user.role == "HSE_OFFICER":
            return self.queryset.filter(incident__reported_by=user)
        return self.queryset.none()
    
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(recipient=self.request.user)

    def perform_create(self, serializer):
        serializer.save()


