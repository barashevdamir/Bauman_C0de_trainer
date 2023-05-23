from django.shortcuts import render, HttpResponse

from .models import *

def index(request):
  tasks = Tasks.objects.all()
  
  return render(request, 'home/index.html', {
    'tasks': tasks,
    'auth':True,

  })
