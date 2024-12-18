from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .formulario import *
from .models import *
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    "error": 'El nombre de usuario ya existe.'
                })
    return render(request, 'signup.html', {
        "error": 'Las contraseñas no coinciden.'
    })

@login_required
def tasks(request):
    tareas_personales = Task.objects.filter(user=request.user, is_personal=True)
    tareas_compartidas = Task.objects.filter(user=request.user, is_personal=False)
    
    return render(request, 'tasks.html', {
        'tareas_personales': tareas_personales,
        'tareas_compartidas': tareas_compartidas
    })

@login_required
def task_comment(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        form = formTaskComment(request.POST)
        if form.is_valid():
            task_comment = form.save(commit=False)
            task_comment.task = task
            task_comment.user = request.user
            task_comment.save()

            return redirect('task_details', task_id=task.id)
        else:
            return render(request, 'task_details.html', {
                'task': task,
                'form': form,
                'error': 'El comentario no es válido.'
            })

    else:
        form = formTaskComment()

    return render(request, 'task_details.html', {'task': task, 'form': form})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if request.method == 'POST':
        form = formTask(request.POST, instance=task)  
        if form.is_valid():
            form.save()  
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

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)    
    if request.user == task.user:
        task.delete()  
        return redirect('tasks')  
    else:
        return redirect('tasks')

def tareatodos(request):
    tareas = Task.objects.filter(is_personal=False)
    return render(request, 'taskall.html', {'tasks': tareas})

def task_details(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    
    if request.method == 'POST':
        form = formTaskComment(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()  

            return redirect('task_details', task_id=task.id)  

    else:
        form = formTaskComment()

    comments = task.comments.all()

    return render(request, 'task_details.html', {
        'task': task,
        'form': form,
        'comments': comments
    })


@login_required
def new_tasks(request):
    if request.method == 'POST':
        form = formTask(request.POST)
        if form.is_valid():
            nueva_tarea = form.save(commit=False)
            nueva_tarea.user = request.user
            nueva_tarea.save()

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
