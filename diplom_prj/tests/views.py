from django.shortcuts import render

def tests(request):
  return render(request, 'tests/tests.html')
