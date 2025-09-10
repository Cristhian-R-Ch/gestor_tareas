from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm


@login_required
def lista_tareas(request):
    tareas = Task.objects.filter(user=request.user).order_by('due_date')
    return render(request, 'tareas/lista.html', {'tareas': tareas})


@login_required
def nueva_tarea(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.user = request.user
            tarea.save()
            return redirect('tareas:lista')
    else:
        form = TaskForm()
    return render(request, 'tareas/form.html', {'form': form, 'accion': 'Nueva'})


@login_required
def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Task, id=tarea_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('tareas:lista')
    else:
        form = TaskForm(instance=tarea)
    return render(request, 'tareas/form.html', {'form': form, 'accion': 'Editar'})


@login_required
def borrar_tarea(request, tarea_id):
    tarea = get_object_or_404(Task, id=tarea_id, user=request.user)
    if request.method == 'POST':
        tarea.delete()
        return redirect('tareas:lista')
    return render(request, 'tareas/confirmar_borrar.html', {'tarea': tarea})


@login_required
def toggle_completed(request, pk):
    tarea = get_object_or_404(Task, pk=pk, user=request.user)
    tarea.is_completed = not tarea.is_completed
    tarea.save()
    return redirect('tareas:lista')