from django.urls import path
from . import views

app_name = 'tareas'

urlpatterns = [
    path('', views.TaskListView.as_view(), name='lista'),  # <-- usar .as_view() para CBV
    path('nueva/', views.TaskCreateView.as_view(), name='nueva'),
    path('editar/<int:pk>/', views.TaskUpdateView.as_view(), name='editar'),
    path('borrar/<int:pk>/', views.TaskDeleteView.as_view(), name='borrar'),
    path('toggle/<int:pk>/', views.toggle_completed, name='toggle'),
    path('guest/', views.login_guest, name='guest_login'),
    path('demo-api/', views.demo_api, name='demo_api'),
]
