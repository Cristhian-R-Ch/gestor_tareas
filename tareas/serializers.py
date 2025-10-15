from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    dias_restantes = serializers.ReadOnlyField()

    class Meta:
        model = Task
        # Campos mostrados en APIREST
        fields = [
            'id',
            'title',
            'description',
            'due_date',
            'is_completed',
            'priority',
            'dias_restantes'
        ]
        read_only_fields = ['dias_restantes']
