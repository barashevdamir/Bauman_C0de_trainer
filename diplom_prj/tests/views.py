from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.http import JsonResponse
from .models import Test, Question, Result
from json import loads
from collections import Counter
from math import floor
from diplom.choices_classes import Status

def test_list(request):
  test_list = Test.objects.filter(status=Status.PUBLISHED)
  
  if request.GET:
    test_list = test_list.order_by(request.GET.get('order_by'))
    if request.GET.get('language') != 'all':
      test_list = test_list.filter(prog_language=request.GET.get('language'))
    if request.GET.get('difficulty') == 'all':
      pass
    elif request.GET.get('difficulty') == 'easy':
      test_list = test_list.filter(experience__lte = 1)
    elif request.GET.get('difficulty') == 'medium':
      test_list = test_list.filter(experience = 2)
    elif request.GET.get('difficulty') == 'hard':
      test_list = test_list.filter(experience = 3)
    if request.GET.get('tag') != 'all':
      test_list = test_list.filter(tags = request.GET.get('tag'))

  paginator = Paginator(test_list, 10)
  page_number = request.GET.get('page')
  try:
    tests = paginator.page(page_number)
  except PageNotAnInteger:
    tests = paginator.page(1)
  except EmptyPage:
    tests = paginator.page(paginator.num_pages)

  if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    if list(test_list) != []:
      return render(
      request, 
      'tests/tests_list.html',
      {'tests': tests}
      )
    else:
      return render(
      request, 
      'base/empty_lists.html',
      {'empty': 'tests'}
      )
  else:
    return render(
      request, 
      'tests/tests.html',
      {'tests': tests}
      )

def test(request, id):
  test = get_object_or_404(
    Test,
    id=id,
    # status=Status.PUBLISHED 
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
      'id': quest.id,
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

def save_result(request, id):
  if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    # не очень приятная обработка данных, проблема в их отправке в кривом виде
    data = dict(request.POST.lists())
    answers = loads(data['answers'][0]) #должно сразу приходить в почти таком виде
    user = request.user
    test = Test.objects.get(id=id)
    correct_answers = 0
    incorrect_answers = 0
    unanswered = 0
    multiplier = 100/test.question_count()
    for key in answers.keys():
      answers_list =[]
      question = Question.objects.get(id=key)
      answers_QuerySet = question.get_correct_answers()
      for ans in answers_QuerySet:
        answers_list.append(ans.text)
      if question.answer_type == 'SC' or question.answer_type == 'MC':
        if  Counter(answers[key]) == Counter(answers_list):
          correct_answers += 1
        elif answers[key][0] == None:
          unanswered += 1
        else:
          incorrect_answers += 1
      else:
        if answers[key][0] in answers_list:
           correct_answers += 1
        elif answers[key][0] == None:
          unanswered += 1
        else:
          incorrect_answers += 1 
    score = floor(correct_answers*multiplier)
    passed = None
    exp_gain = 0
    if score >= test.score_to_pass:
      passed = True
      exp_gain = test.experience 
    else:
      passed = False
    try:
      Result.objects.create(
        user = user,
        test = test,
        passed = passed,
        score = score,
        exp_gain = exp_gain
      )
    except ValueError:
      pass
    result = {
      'test': test.title,
      'passed': passed,
      'score': score,
      'exp_gain': exp_gain,
      'correct': correct_answers,
      'incorrect': incorrect_answers,
      'unanswered': unanswered
    }
    return JsonResponse(result)
    
def result(request, id):
  return render(
    request,
    'tests/result.html', 
  )

