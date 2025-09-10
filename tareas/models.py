from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from datetime import date


class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    due_date = models.DateField(verbose_name="Fecha de vencimiento")
    is_completed = models.BooleanField(default=False, verbose_name="Completada")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")

    def __str__(self):
        return self.title

    @property
    def dias_restantes(self):
        """Devuelve los días restantes hasta la fecha de vencimiento."""
        if self.due_date:
            return (self.due_date - date.today()).days
        return None
