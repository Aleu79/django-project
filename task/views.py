from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpRequest


# Create your views here.

def home(request):
    return render(request, 'home.html',)
def signup(request):
    
    if request.method == 'GET':
        print('enviando formulario')
    else:
        print(request.POST)
        print('recibiendo datos')
    return render(request, 'signup.html',)

 


 