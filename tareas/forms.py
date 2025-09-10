from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        label="Fecha de vencimiento"
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'is_completed']
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'is_completed': 'Completada',
        }
