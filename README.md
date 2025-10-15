# Gestor de Tareas
Proyecto de ejemplo desarrollado en **Django**, que permite gestionar tareas con funcionalidades de crear, editar, eliminar y marcar tareas como completadas.

---
## Características
- Registro de tareas con título, Descripcion, Prioridad y fecha de vencimiento.
- Cambiar el estado de una tarea (completada / incompleta).
- Editar o eliminar tareas existentes.
- Filtrar Tareas por Fecha de vencimiento, Estado y Busqueda por Titulo de Tarea.
- Acceso mediante usuario registrado o como invitado.
- Interfaz sencilla con estilos CSS.

---
## Enlace a GitHub
- https://github.com/Cristhian-R-Ch/gestor_tareas

---
- 
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
