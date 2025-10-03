from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task
from datetime import date

class TaskModelTests(TestCase):

    def setUp(self):
        #Usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='12345')
        #Tarea de prueba asociada al usuario
        self.task = Task.objects.create(
            title='Tarea de prueba',
            due_date=date.today(),
            user=self.user
        )

    #Test método __str__
    def test_str_method(self):
        self.assertEqual(str(self.task), 'Tarea de prueba')

    #Test propiedad dias_restantes
    def test_dias_restantes(self):
        self.assertEqual(self.task.dias_restantes, 0)

class TaskViewTests(TestCase):

    def setUp(self):
        #Crear usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='12345')
        #Crear tarea de prueba
        self.task = Task.objects.create(
            title='Tarea de prueba',
            due_date=date.today(),
            user=self.user
        )

    #Test que la lista de tareas es accesible
    def test_task_list_view(self):
        #Hacer login primero
        self.client.login(username='testuser', password='12345')
        url = reverse('tareas:lista')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tareas/lista.html')
        self.assertContains(response, 'Tarea de prueba')

    #Test crear tarea
    def test_create_task_view(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('tareas:nueva')
        data = {
            'title': 'Otra tarea',
            'description': 'Descripción de prueba',
            'due_date': date.today(),
            'is_completed': False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirige al listar
        self.assertTrue(Task.objects.filter(title='Otra tarea').exists())

    #Test editar tarea
    def test_update_task_view(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('tareas:editar', kwargs={'pk': self.task.pk})
        data = {
            'title': 'Tarea editada',
            'description': self.task.description or '',  # <-- corregido aquí
            'due_date': self.task.due_date,
            'is_completed': self.task.is_completed
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Tarea editada')

    #Test borrar tarea
    def test_delete_task_view(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('tareas:borrar', kwargs={'pk': self.task.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    #Test toggle completado
    def test_toggle_completed_view(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('tareas:toggle', kwargs={'pk': self.task.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)
