from django.shortcuts import render, get_object_or_404, HttpResponse
import os
import epicbox
import tempfile
import shutil
from .models import *

def taskspage(request):
  tasks = Tasks.objects.all()

  if request.GET:
    get_turple = request.GET

    if request.GET.get('order_by', False):
      tasks = tasks.order_by(get_turple['order_by'])

    if request.GET.get('level', False):
      tasks = tasks.filter(level=get_turple['level'])

    if request.GET.get('language', False):
      tasks_arr = []
      for task in tasks:
        tmp_arr = task.languages.split()
        for el in tmp_arr:
          if el == get_turple['language']:
            tasks_arr.append(task.name)
      if get_turple['language'] != 'All':
        tasks = tasks.filter(name__in=tasks_arr)

    if request.GET.get('tag', False):
      tasks_arr = []
      for task in tasks:
        tmp_arr = task.tags.split()
        for el in tmp_arr:
          if el == get_turple['tag']:
            tasks_arr.append(task.name)
      tasks = tasks.filter(name__in=tasks_arr)

  if not tasks:
    tasks = False
  
  return render(request, 'tasks/tasks.html', {
    'title' : 'Tasks',
    'tasks': tasks,
  })

def task(request, id):
  task = get_object_or_404(
    Tasks,
    id=id,
    #status=Test.Status.DRAFT
  )
  if request.POST and request.headers.get('x-requested-with') == 'XMLHttpRequest':
    datas = dict(request.POST.lists())

    language = str.lower(datas['language'][0])

    code = datas['code'][0]
    if language =='python':
      file_path = "media/temp/task" + str(id) + ".py"
      program_file = open(file_path, "w")
      program_file.write(code)
      program_file.close()

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

      pytest_code_path = "media/temp/test" + str(id) + ".py"
      pytest_code = ''

      with open(pytest_code_path) as file:
        pytest_code_list = file.readlines()
        for item in pytest_code_list:
          pytest_code = pytest_code + item


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