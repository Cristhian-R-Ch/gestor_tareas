from django.contrib import admin

# Register your models here.
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'due_date', 'is_completed', 'dias_restantes')
    list_filter = ('is_completed', 'due_date', 'user')
    search_fields = ('title', 'description')
