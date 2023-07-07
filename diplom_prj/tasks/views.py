from django.shortcuts import render, get_object_or_404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
import epicbox
import tempfile
import shutil
from .models import *
from .task_check import *
from diplom.choices_classes import Status, ProgLanguage

def taskspage(request):
  tasks_list = Tasks.objects.filter(status=Status.PUBLISHED)

  if request.GET:
    tasks_list = tasks_list.order_by(request.GET.get('order_by'))
    # if request.GET.get('language') != 'all':
    #   tasks = test_list.filter(prog_language=request.GET.get('language'))
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

def task(request, id):
  task = get_object_or_404(
    Tasks,
    id=id,
    # status=Status.PUBLISHED 
  )
  if request.POST and request.headers.get('x-requested-with') == 'XMLHttpRequest':

    form_data = dict(request.POST.lists())
    language = str.lower(form_data['language'][0])
    code = form_data['code'][0]

    if language =='python':
      task_language = TaskLanguage.objects.get(task=task, prog_language=ProgLanguage.PYTHON)
      file_path = task_language.test_file.path
      # with open(file_path, 'w') as program_file:
      #   program_file.write(code)
      # print(file_path)

    if language == "php":
      pass

    elif language == "python":

      epicbox.configure(
        profiles=[
          epicbox.Profile('python', 'python')
        ]
      )

      files = [{'name': 'main.py', 'content': bytes(code, 'utf-8')}]
      limits = {'cputime': 1, 'memory': 64}
      output = epicbox.run('python', 'python3 main.py', files=files, limits=limits)

      # Создаем временную директорию для работы с файлами
      temp_dir = tempfile.mkdtemp()

      # Подготовка кода тестов

      task_language = TaskLanguage.objects.get(task=task, prog_language=ProgLanguage.PYTHON)

      pytest_code_path = task_language.test_file.path

      with open(pytest_code_path) as file:
        pytest_code_list = file.readlines()
        pytest_code = ''.join(pytest_code_list)


      # test_code = pytest_code
      test_code = code + '\n\n'+ pytest_code


      # Настройка Epicbox

      epicbox.configure(profiles=[
          epicbox.Profile('python', 'my_python_image')
      ])

      files = [{'name': 'test_code.py', 'content': bytes(test_code, 'utf-8')}]
      limits = {'cputime': 1, 'memory': 128}

      # Создание контейнера

      container = epicbox.run('python', 'python3 -m pytest test_code.py',
                              files=files,
                              limits=limits)
      print(container)

      # Копируем результаты из контейнера во временную директорию

      stdout_path = os.path.join(temp_dir, 'stdout')
      stderr_path = os.path.join(temp_dir, 'stderr')

      with open(stdout_path, 'wb') as stdout_file:
        stdout_file.write(container['stdout'])

      with open(stderr_path, 'wb') as stderr_file:
        stderr_file.write(container['stderr'])

      # Оценка результата pytest

      if container['exit_code'] == 0:
        print("Тесты пройдены успешно.")
      else:
        print("Тесты провалены.")

      # Удаляем временную директорию

      shutil.rmtree(temp_dir)

      return render(request, 'tasks/training.html', {'id': id, 'code': code, 'output': output})

    elif language == "node":
        pass

    elif language == "c":
        pass

    elif language == "cpp":
        pass
    
  return render(
    request, 
    'tasks/training.html',
    {'task': task})