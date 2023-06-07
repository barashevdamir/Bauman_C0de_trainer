from django.shortcuts import render, get_object_or_404
from .models import Test

def test_list(request):
  tests = Test.objects.all()
  return render(
    request, 
    'tests/tests.html',
    {'tests': tests}
    )

def test(request, pk):
  test = get_object_or_404(
    Test,
    id=pk,
    status=Test.Status.PUBLISHED
  )
  return render(
    request,
    'tests/test.html',
    {'test': test}
  )

def result(request):
  return render(
    request,
   'tests/result.html',  
  )

