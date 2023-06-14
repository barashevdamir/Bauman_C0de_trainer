from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage

from .models import Test

def test_list(request):
  test_list = Test.objects.all()
  paginator = Paginator(test_list, 1)
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

def test(request, id):
  test = get_object_or_404(
    Test,
    id=id,
    status=Test.Status.DRAFT
  )
  question_list = []
  for quest in test.get_questions():
    answers = []
    codes =[]
    for code in quest.get_codes():
      codes.append(code.text)
    for ans in quest.get_answers():
      answers.append(ans.text)
    question_list.append({
      'prompt': quest.prompt,
      'answer_type': quest.answer_type,
      'codes': codes, 
      'answers': answers
    })
  paginator = Paginator(question_list, 1)
  page_number = request.GET.get('question')
  try:
    questions = paginator.page(page_number)
  except InvalidPage:
    questions = paginator.page(1)
  return render(
    request,
    'tests/test.html',
    {'test': test, 'questions': questions}
  )

def result(request):
  return render(
    request,
   'tests/result.html',  
  )

