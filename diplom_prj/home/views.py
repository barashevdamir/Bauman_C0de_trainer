from django.shortcuts import render, HttpResponse

def index(request):
  return render(request, 'home/index.html', {
    'auth':True,
  })

def homepage(request):
  return render(request, 'home/homepage.html')