from django.shortcuts import render, HttpResponse

def index(request):
  return render(request, 'tasks/tasks.html', {
    'auth':True,
  })

def homepage(request):
  return render(request, 'tasks/homepage.html')