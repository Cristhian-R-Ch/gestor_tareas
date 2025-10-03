from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Task
from .forms import TaskForm, RegisterForm
 
#Lista de tareas
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tareas/lista.html'
    context_object_name = 'tareas'

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        
        # Filtrado por estado
        estado = self.request.GET.get('estado')
        if estado == 'completadas':
            queryset = queryset.filter(is_completed=True)
        elif estado == 'incompletas':
            queryset = queryset.filter(is_completed=False)
        
        # Busqueda por título
        buscar = self.request.GET.get('buscar')
        if buscar:
            queryset = queryset.filter(title__icontains=buscar)
            
        # Ordenar por fecha
        orden = self.request.GET.get('orden')
        if orden == 'desc':
            queryset = queryset.order_by('-due_date')
        else:
            queryset = queryset.order_by('due_date')

        return queryset

#Crear tarea
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tareas/form.html'
    success_url = reverse_lazy('tareas:lista')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = 'Crear'
        return context

#Editar tarea
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tareas/form.html'
    success_url = reverse_lazy('tareas:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = 'Editar'
        return context

#Borrar tarea
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tareas/confirmar_borrar.html'
    success_url = reverse_lazy('tareas:lista')

#Toggle estado
def toggle_completed(request, pk):
    tarea = Task.objects.get(pk=pk, user=request.user)
    tarea.is_completed = not tarea.is_completed
    tarea.save()
    return redirect('tareas:lista')

#Login como invitado
def login_guest(request):
    demo_user = User.objects.get(username='demo')
    login(request, demo_user)
    return redirect('tareas:lista')

#Logout
def logout_view(request):
    logout(request)
    return redirect('login')

#Register
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user) 
            return redirect('tareas:lista') 
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
