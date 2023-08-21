from rest_framework import permissions


class IsAirlineCompany(permissions.BasePermission):
    """
    Allows access only to users with the role 'AirlineCompany'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_role.role_name == 'Airline Company'

class IsCustomer(permissions.BasePermission):
    """
    Allows access only to users with the role 'Customer'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_role.role_name == 'Customer'

class IsAdministrator(permissions.BasePermission):
    """
    Allows access only to users with the role 'Administrator'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_role.role_name == 'Administrator'
