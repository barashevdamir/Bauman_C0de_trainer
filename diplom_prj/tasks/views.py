from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
import epicbox
import tempfile
import shutil
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import *
from .task_check import *
from diplom.choices_classes import Status, ProgLanguage
from django.http import JsonResponse
import os
import subprocess

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

def get_file_content(request):
  file_path = request.GET.get('file_path', '')
  if os.path.isfile(file_path):
    with open(file_path, 'r') as file:
      content = file.read()
    return JsonResponse({'content': content})
  else:
    return JsonResponse({'error': 'File not found'}, status=404)

@login_required
def task(request, id):

  task = get_object_or_404(
    Tasks,
    id=id,
    status=Status.PUBLISHED
  )

  context = {'task': task}

  if request.POST and request.headers.get('x-requested-with') == 'XMLHttpRequest':

    form_data = dict(request.POST.lists())
    language = str.lower(form_data['language'][0])
    code = form_data['code'][0]
    file_name = 'task' + str(task.id)


    if language =='py':

      if request.user.is_authenticated:
        directory = f'{settings.MEDIA_ROOT}/tasks/task_id{task.id}/{request.user.username}'
        if not os.path.exists(directory):
          os.makedirs(directory)
        # Save the code in a .py file
        with open(f"{directory}/{file_name}.py", "w") as file:
          file.write(code)

      epicbox.configure(
        profiles=[
          epicbox.Profile('python', 'python')
        ]
      )

      # Создаем временную директорию для работы с файлами
      temp_dir = tempfile.mkdtemp()

      # Подготовка кода тестов

      task_language = TaskLanguage.objects.get(task=task, prog_language=ProgLanguage.PYTHON)

      pytest_code = task_language.test_file.read()
    
      # test_code = pytest_code
      test_code =  bytes(code, 'utf-8') + b'\n\n'+ pytest_code


      # Настройка Epicbox

      epicbox.configure(profiles=[
          epicbox.Profile('python', 'python')
      ])

      files = [{'name': 'test_code.py', 'content': test_code}]
      limits = {'cputime': 1, 'memory': 64}

      # Создание контейнера

      container = epicbox.run('python', 'python3 -m unittest test_code.py',
                              files=files,
                              limits=limits)


      # Копируем результаты из контейнера во временную директорию

      stdout_path = os.path.join(temp_dir, 'stdout')
      stderr_path = os.path.join(temp_dir, 'stderr')

      with open(stdout_path, 'wb') as stdout_file:
        stdout_file.write(container['stdout'])

      with open(stderr_path, 'wb') as stderr_file:
        stderr_file.write(container['stderr'])

      # Оценка результата pytest

      request.session['code'] = code

      passed = False
      exp_gain = 0

      if container['exit_code'] == 0:
        passed = True
        exp_gain = task.level*3
        if request.user.is_authenticated:
          with open(f"{directory}/{file_name}_result.txt", "w") as file:
            file.write("Тесты пройдены успешно.")
      else:
        if request.user.is_authenticated:
          with open(f"{directory}/{file_name}_result.txt", "w") as file:
            file.write("Тесты провалены.")

      result = Result(user=request.user, task=task, code=code, file_name=file_name, prog_language=ProgLanguage.PYTHON, passed=passed, exp_gain=exp_gain)
      result.save()

      # Удаляем временную директорию

      shutil.rmtree(temp_dir)

    elif language == "js":

      if request.user.is_authenticated:
        directory = f'{settings.MEDIA_ROOT}/tasks/task_id{task.id}/{request.user.username}'
        if not os.path.exists(directory):
          os.makedirs(directory)
        # Save the code in a .js file
        with open(f"{directory}/{file_name}.js", "w") as file:
          file.write(code)

      # Configure Epicbox for JavaScript
      epicbox.configure(
        profiles=[
          epicbox.Profile('nodejs', 'nodejs')
        ]
      )

      # Create a temporary directory for file operations
      temp_dir = tempfile.mkdtemp()

      # Prepare the test code
      task_language = TaskLanguage.objects.get(task=task, prog_language=ProgLanguage.JAVASCRIPT)
      test_code = task_language.test_file.read()

      # Concatenate the code and the test code
      test_code = bytes(code, 'utf-8') + b'\n\n' + test_code

      # Configure Epicbox for JavaScript
      epicbox.configure(
        profiles=[
          epicbox.Profile('nodejs', 'nodejs')
        ]
      )

      files = [{'name': 'test_code.js', 'content': test_code}]
      limits = {'cputime': 1, 'memory': 64}

      # Create a container
      container = epicbox.run('nodejs', 'node test_code.js',
                              files=files,
                              limits=limits)

      # Copy the container results to the temporary directory
      stdout_path = os.path.join(temp_dir, 'stdout')
      stderr_path = os.path.join(temp_dir, 'stderr')

      with open(stdout_path, 'wb') as stdout_file:
        stdout_file.write(container['stdout'])

      with open(stderr_path, 'wb') as stderr_file:
        stderr_file.write(container['stderr'])

      # Evaluate the test results
      request.session['code'] = code

      passed = False

      if container['exit_code'] == 0:
        passed = True
        if request.user.is_authenticated:
          with open(f"{directory}/{file_name}_result.txt", "w") as file:
            file.write("Tests passed successfully.")
      else:
        if request.user.is_authenticated:
          with open(f"{directory}/{file_name}_result.txt", "w") as file:
            file.write("Tests failed.")

      result = Result(user=request.user, task=task, code=code, file_name=file_name,
                      prog_language=ProgLanguage.JAVASCRIPT, passed=passed)
      result.save()

      # Remove the temporary directory
      shutil.rmtree(temp_dir)

    elif language == "c":
        pass

    elif language == "cpp":
        pass

  # проверка, есть ли код и выходные данные

  file_name = 'task' + str(task.id)
  directory = f'{settings.MEDIA_ROOT}/tasks/task_id{task.id}/{request.user.username}'

  try:
    with open(f"{directory}/{file_name}.py", "r") as file:
      code = file.read()
    context['code'] = code
  except Exception as e:
    print(f"Error reading code file: {e}")
    context['code'] = ''

  try:
    with open(f"{directory}/{file_name}_result.txt", "r") as file:
      output = file.read()
    context['output'] = output
  except Exception as e:
    print(f"Error reading output file: {e}")
    context['output'] = ''

  task_language = TaskLanguage.objects.get(task=task, prog_language=ProgLanguage.PYTHON)

  tasks_solution_code = task_language.solution_file.read()
  context['solution'] = tasks_solution_code.decode()

  return render(request, 'tasks/training.html',  context)
