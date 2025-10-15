from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import TaskViewSet

# Rutas bajo el prefijo /api/
router = DefaultRouter() # Enrutador para generar automaticamente las rutas CRUD
router.register(r'tareas', TaskViewSet, basename='tarea') #viewset bajo prefijo tareas

urlpatterns = [
    path('', include(router.urls)),
]
