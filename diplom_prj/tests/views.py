from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Test

def test_list(request):
  test_list = Test.objects.all()
  paginator = Paginator(test_list, 10)
  page_number = request.GET.get('page')
  try:
    tests = paginator.page(page_number)
  except PageNotAnInteger:
    tests = paginator.page(1)
  except EmptyPage:
    tests = paginator.page(paginator.num_pages)
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
  paginator = Paginator(test, 1)
  page_number = request.GET.get('page')
  try:
    test = paginator.page(page_number)
  except PageNotAnInteger:
    test = paginator.page(1)
  except EmptyPage:
    test = paginator.page(paginator.num_pages)
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

