from rest_framework.permissions import BasePermission

class IsHSEOfficer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "HSE_OFFICER"

class IsHSEManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "HSE_MANAGER"

class IsHSESupervisor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "HSE_SUPERVISOR"

class IsOwnerOrSupervisorOrManager(BasePermission):
    """
    Officers can see their own incidents
    Supervisors can see incidents assigned to them
    Managers can see all
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == "HSE_MANAGER":
            return True
        elif request.user.role == "HSE_SUPERVISOR":
            return obj.assigned_supervisor == request.user
        elif request.user.role == "HSE_OFFICER":
            return obj.reported_by == request.user
        return False