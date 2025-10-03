from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        label="Fecha de vencimiento",
        required=False
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'is_completed']
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'due_date': 'Fecha de vencimiento',
            'priority': 'Prioridad',
            'is_completed': 'Completada',
        }

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        help_texts = {
            'username': '', 
        }
