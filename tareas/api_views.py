from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    Viewset permite realizar CRUD en modelo Task
    Requiere autenticacion y entrega tareas relacionadas al usuario autentificado
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Retorna las tareas del usuario autentificado
        """
        return Task.objects.filter(user=self.request.user).order_by('-due_date')

    def perform_create(self, serializer):
        """
        Asigna automáticamente el usuario autentificado al crear una nueva tarea
        """
        serializer.save(user=self.request.user)
