from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from diplom.choices_classes import Status, ProgLanguage
from django.conf import settings
from .models import *
from .task_check import *

def taskspage(request):
  tasks_list = Tasks.objects.filter(status=Status.PUBLISHED)

  if request.GET:
    tasks_list = tasks_list.order_by(request.GET.get('order_by'))
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
      {'tasks': tasks}
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
    {'tasks': tasks}
  )

@login_required
def task(request, id):
  task = get_object_or_404(Tasks, id=id, status=Status.PUBLISHED)
  context = {'task': task}
  user = request.user

  if request.POST and request.headers.get('x-requested-with') == 'XMLHttpRequest':
    form_data = dict(request.POST.lists())
    language = form_data['language'][0]
    code = form_data['code'][0]

    file_name = create_file(task, user, code, language)
    test_code = TaskLanguage.objects.get(task=task, prog_language=language).test_file.read()
    epic_code = get_epic_code(code, language, test_code)
    result = run_epic_code(epic_code, language)
    check = check_result(result, task.level)
    result_message = check['message']
    message_file = create_file(task, user, result_message, 'txt')
    
    res = Result(
      user=user, 
      task=task, 
      code=code, 
      file_name=file_name,
      prog_language=language, 
      passed=check['passed'], 
      exp_gain=check['exp_gain'],
      result=result_message
    )
    res.save()
  
  handle_solution_code_and_output(task, user, context)
  return render(request, 'tasks/training.html', context)


def handle_solution_code_and_output(task, user, context):
  file_name = f'{task.slug}-id{task.id}'
  directory = '{0}/results/{1}_id{2}/{3}_id{4}'.format(settings.MEDIA_ROOT, user.username, user.id, task.slug, task.id)

  if task.languages.filter(prog_language=ProgLanguage.PYTHON).exists():
    # Retrieve Python solution, code, and output
    task_language = TaskLanguage.objects.get(task=task, prog_language=ProgLanguage.PYTHON)
    tasks_solution_code = task_language.solution_file.read()
    context['solution'] = tasks_solution_code.decode()

    try:
      with open(f"{directory}/{file_name}.py", "r") as file:
        code = file.read()
      context['code'] = code
    except Exception as e:
      print(f"Error reading code file: {e}")
      context['code'] = ''
    
    try:
      with open(f"{directory}/{file_name}.txt", "r") as file:
        output = file.read()
      context['output'] = output
    except Exception as e:
      print(f"Error reading output file: {e}")
      context['output'] = ''

  elif task.languages.filter(prog_language=ProgLanguage.JAVASCRIPT).exists():
    # Retrieve JavaScript solution, code, and output
    task_language = TaskLanguage.objects.get(task=task, prog_language=ProgLanguage.JAVASCRIPT)
    tasks_solution_code = task_language.solution_file.read()
    context['solution'] = tasks_solution_code.decode()

    try:
      with open(f"{directory}/{file_name}.js", "r") as file:
        code = file.read()
      context['code'] = code
    except Exception as e:
      print(f"Error reading code file: {e}")
      context['code'] = ''

    try:
      with open(f"{directory}/{file_name}.txt", "r") as file:
        output = file.read()
      context['output'] = output
    except Exception as e:
      print(f"Error reading output file: {e}")
      context['output'] = ''
