from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import AuthenticationForm
from .models import Task
from .forms import TaskForm, RegisterForm
from rest_framework_simplejwt.tokens import RefreshToken

# -----------------------
# CRUD TAREAS
# -----------------------

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

        # Busqueda por titulo
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

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tareas/form.html'
    success_url = reverse_lazy('tareas:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = 'Editar'
        return context

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tareas/confirmar_borrar.html'
    success_url = reverse_lazy('tareas:lista')

def toggle_completed(request, pk):
    tarea = Task.objects.get(pk=pk, user=request.user)
    tarea.is_completed = not tarea.is_completed
    tarea.save()
    return redirect('tareas:lista')


# -----------------------
# LOGIN | LOGOUT | REGISTER
# -----------------------

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirigir a next o por defecto a lista de tareas
            next_url = request.POST.get('next') or reverse_lazy('tareas:lista')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    next_url = request.GET.get('next', '')
    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    logout(request)
    return redirect('login')


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


# Login invitado
def login_guest(request):
    demo_user = User.objects.get(username='demo')
    login(request, demo_user)
    return redirect('tareas:lista')


# -----------------------
# API
# -----------------------

@login_required
def demo_api(request):
    # Generar token usuario actual
    refresh = RefreshToken.for_user(request.user)
    access_token = str(refresh.access_token)

    return render(request, 'tareas/demo_api.html', {'token': access_token})
