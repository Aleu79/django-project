from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .formulario import formTask
# Create your views here.


def home(request):
    return render(request, 'home.html',)


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # register user
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    "error": 'username already exits'
                })
    return render(request, 'signup.html', {
        "error": 'password do not match'
    })


def tasks(request):
    return render(request, 'tasks.html')


def new_tasks(request):
   if request.method == "GET":
        return render(request, 'new_tasks.html', {
        'form': formTask
        })
   elif request.method == "POST":
       print(request.POST)
       return render(request, 'new_tasks.html', {
       'form': formTask
    })  
   else:
    return render(request, "puta")


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                "error": 'username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')
