from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir:
    - Lectura (GET, HEAD, OPTIONS) a cualquier usuario autenticado
    - Escritura (POST, PUT, PATCH, DELETE) solo a administradores
    """
    
    def has_permission(self, request, view):
        # Primero verificar que el usuario esté autenticado
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Permitir métodos de lectura (GET, HEAD, OPTIONS) a todos
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Solo administradores pueden hacer cambios
        return request.user.is_staff or request.user.is_superuser
