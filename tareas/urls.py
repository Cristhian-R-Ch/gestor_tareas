from django.urls import path
from . import views

app_name = 'tareas'

urlpatterns = [
    path('', views.lista_tareas, name='lista'),
    path('nueva/', views.nueva_tarea, name='nueva'),
    path('editar/<int:tarea_id>/', views.editar_tarea, name='editar'),
    path('borrar/<int:tarea_id>/', views.borrar_tarea, name='borrar'),
    path('toggle/<int:pk>/', views.toggle_completed, name='toggle'),
    path('guest/', views.login_guest, name='guest_login'),
]
