from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from diplom.choices_classes import Status
from django.conf import settings
from json import loads
from .models import *
from .task_check import *

def taskspage(request):
  tasks_list = Tasks.objects.filter(status=Status.PUBLISHED)

  if request.GET:
    tasks_list = tasks_list.order_by(request.GET.get('order_by'))
    if request.GET.get('login') != 'all':
      tasks_list = tasks_list.filter(login=loads(request.GET.get('login')))
    if request.GET.get('lvl') != 'all':
      tasks_list = tasks_list.filter(level = request.GET.get('lvl'))
    if request.GET.get('tag') != 'all':
      tasks_list = tasks_list.filter(tags = request.GET.get('tag'))
    if request.GET.get('language') != 'all':
      lang = TaskLanguage.objects.filter(prog_language = request.GET.get('language'))
      tasks_list = tasks_list.filter(languages__in = lang)

  paginator = Paginator(tasks_list, 10)
  page_number = request.GET.get('page')
  try:
    tasks = paginator.page(page_number)
  except PageNotAnInteger:
    tasks = paginator.page(1)
  except EmptyPage:
    tasks = paginator.page(paginator.num_pages)

  if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    if list(tasks_list) != []:
      return render(
      request,
      'tasks/tasks_list.html',
      {'tasks': tasks, 'auth': request.user.is_authenticated}
      )
    else:
      return render(
      request,
      'base/empty_lists.html',
      {'empty': 'tasks'}
      )
  return render(
    request,
    'tasks/tasks.html',
    {'tasks': tasks, 'auth': request.user.is_authenticated}
  )

def task(request, id):
  task = get_object_or_404(Tasks, id=id, status=Status.PUBLISHED)
  user = request.user

  if request.GET and request.headers.get('x-requested-with') == 'XMLHttpRequest':
    lang = request.GET.get('language')
    if request.GET.get('code-editor') == 'need' and request.user.is_authenticated:
      try:
        code = Result.objects.filter(task=task, user=user, prog_language=lang).latest('date').result_code.read().decode()
      except (Result.DoesNotExist, FileNotFoundError, ValueError):
        code = ''
    else:
      code = ''
    if request.GET.get('output') == 'need' and request.user.is_authenticated:
      try:
        output = Result.objects.filter(task=task, user=user, prog_language=lang).latest('date').result_message.read().decode()
      except (Result.DoesNotExist, FileNotFoundError, ValueError):
        output = ''
    else:
      output = ''
    if request.GET.get('solution-editor') == 'need':
      try:
        solution = TaskLanguage.objects.get(task=task, prog_language=lang).solution_file.read().decode()
      except (ValueError, FileNotFoundError):
        solution = ''
    else:
      solution = ''
    return JsonResponse({
      'code-editor': code, 
      'output': output,
      'solution-editor': solution
    })
  
  return render(request, 'tasks/training.html', {'task': task})

def save_result(request, id):
  if request.POST and request.headers.get('x-requested-with') == 'XMLHttpRequest':
    task = get_object_or_404(Tasks, id=id, status=Status.PUBLISHED)
    user = request.user
    form_data = dict(request.POST.lists())
    language = form_data['language'][0]
    code = form_data['code'][0]

    code_file = create_file(task, user, code, language)
    test_code = TaskLanguage.objects.get(task=task, prog_language=language).test_file.read()
    epic_code = get_epic_code(code, language, test_code)
    result = run_epic_code(epic_code, language)
    check = check_result(result, task.level)
    message = check['message']
    message_file = create_file(task, user, message, 'txt')
    
    if request.user.is_authenticated:
      Result.objects.create(
        user=user, 
        task=task,
        prog_language=language, 
        passed=check['passed'], 
        exp_gain=check['exp_gain'],
        result_code=code_file.name,
        result_message=message_file.name
      )
    
    return JsonResponse({'output': message})

