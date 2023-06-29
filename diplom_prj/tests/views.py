from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.http import JsonResponse
from .models import Test, Question, Answer, Result
from json import loads
from collections import Counter

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
    questions = {} # для проверки, потом удалить
    # не очень приятная обработка данных, проблема в их отправке в кривом виде
    data = dict(request.POST.lists())
    answers = loads(data['answers'][0]) #должно сразу приходить в почти таком виде
    print(answers) # для проверки, потом удалить
    user = request.user #AnonymousUser, если не авторизирован
    print(user)
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
      questions[str(question.id)] = answers_list # для проверки, потом удалить
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
    score = correct_answers*multiplier
    
    # для проверки, потом удалить
    print(questions)
    print('correct: ', correct_answers)
    print('incorrect: ', incorrect_answers)
    print('unanswered: ', unanswered)
    print(score, '%')
    # 


  return JsonResponse({'text': 'works'})

def result(request, id):
  # print(request.POST)
  # return JsonResponse({'text': 'works'})
  return render(
    request,
   'tests/result.html',  
  )

