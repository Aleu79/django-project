from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .formulario import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.exceptions import ValidationError


def home(request):
    unread_notifications = 0

    if request.user.is_authenticated:
        unread_notifications = TaskNotification.objects.filter(user=request.user, read=False).count()

    return render(request, 'home.html', {
        'unread_notifications': unread_notifications
    })

@login_required(login_url='signup')
def create_task_notification(task, user, message):
    notification = TaskNotification(
        task=task,
        user=user,
        message=message
    )
    notification.save()


@login_required(login_url='signup')
def notifications(request):
    notifications = TaskNotification.objects.filter(user=request.user)

    unread_count = notifications.filter(read=False).count()

    notifications.filter(read=False).update(read=True)

    return render(request, 'notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })


@login_required(login_url='signup')
def mark_as_read(request, notification_id):
    notification = get_object_or_404(TaskNotification, pk=notification_id, user=request.user)
    notification.read = True
    notification.save()
    return redirect('notifications')


def perfil(request):
    if request.user.is_authenticated:
        return render(request, 'perfil.html', {
            'is_authenticated': True,
        })
    else:
        return render(request, 'perfil.html', {
            'is_authenticated': False,
        })

def error_page(request, message="Ha ocurrido un error inesperado"):
    """
    Función para mostrar una página de error con un mensaje personalizado.
    """
    return render(request, 'error_page.html', {'message': message})

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                email = request.POST['gmail']

                if not email or '@' not in email:
                    raise ValidationError("Por favor ingresa un correo válido.")

                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'],
                    email=email
                )
                print(f"Usuario creado: {user.username}, Gmail: {user.email}")
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    "error": 'El nombre de usuario ya existe.'
                })
            except ValidationError as ve:
                return render(request, 'signup.html', {
                    "error": str(ve)
                })
        return render(request, 'signup.html', {
            "error": 'Las contraseñas no coinciden.'
        })
    


@login_required(login_url='signup')
def tasks(request):
    try:
        tareas_personales = Task.objects.filter(user=request.user, is_personal=True)
        tareas_compartidas = Task.objects.filter(user=request.user, is_personal=False)
        
        return render(request, 'tasks.html', {
            'tareas_personales': tareas_personales,
            'tareas_compartidas': tareas_compartidas
        })
    except Exception as e:
        return error_page(request, f'Ocurrió un error al cargar las tareas: {str(e)}')

@login_required(login_url='signup')
def task_details(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task_history = task.taskhistory_set.all()

    if request.method == 'POST':
        form = formTaskComment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()

            add_task_history(task, request.user, "Comentario Agregado")
            
            if request.user != task.user:
                create_task_notification(
                    task,
                    task.user,
                    f"Nuevo comentario en tu tarea '{task.title}' por {request.user.username}: {comment.comment[:50]}..."
                )

            return redirect('task_details', task_id=task.id)

    else:
        form = formTaskComment()

    comments = task.comments.all()

    return render(request, 'task_details.html', {
        'task': task,
        'form': form,
        'comments': comments,
        'task_history': task_history  
    })

@login_required(login_url='signup')
def add_task_history(task, user, action):
    """
    Función para agregar un registro al historial de la tarea.
    """
    history = TaskHistory(task=task, user=user, action=action)
    history.save()


@login_required(login_url='signup')
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if request.method == 'POST':
        form = formTask(request.POST, instance=task)  
        if form.is_valid():
            task = form.save()  

            add_task_history(task, request.user, "Tarea Editada")
            
            if task.is_personal:
                return redirect('tasks')  
            else:
                return redirect('tareatodos')  
        else:
            return render(request, 'edit_task.html', {
                'form': form,
                'error': 'Por favor, corrige los errores.'
            })
    else:
        form = formTask(instance=task)  
    return render(request, 'edit_task.html', {'form': form})

@login_required(login_url='signup')
def delete_task(request, task_id):
    try:
        task = get_object_or_404(Task, pk=task_id)    
        if request.user == task.user:
            add_task_history(task, request.user, "Tarea Eliminada")
            task.comments.all().delete()

            task.delete()  
            return redirect('tasks')  
        else:
            return redirect('tasks')

    except Exception as e:
        return error_page(request, f'Ocurrió un error al intentar eliminar la tarea: {str(e)}')


def tareatodos(request):
    tareas = Task.objects.filter(is_personal=False)
    return render(request, 'taskall.html', {'tasks': tareas})

@login_required(login_url='signup')
def new_tasks(request):
    if request.method == 'POST':
        form = formTask(request.POST)
        if form.is_valid():
            nueva_tarea = form.save(commit=False)
            nueva_tarea.user = request.user
            nueva_tarea.save()
            add_task_history(nueva_tarea, request.user, "Tarea Creada")

            if nueva_tarea.is_personal:
                return redirect('tasks')  
            else:
                return redirect('tareatodos')  
        else:
            return render(request, 'new_tasks.html', {
                'form': form,
                'error': 'Por favor, corrige los errores.'
            })
    else:
        form = formTask()
    return render(request, 'new_tasks.html', {'form': form})

@login_required(login_url='signup')
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password']
        )
        if user is None:
            return render(request, 'signin.html', {
                "error": 'El nombre de usuario o la contraseña son incorrectos.'
            })
        else:
            login(request, user)
            return redirect('tasks')
