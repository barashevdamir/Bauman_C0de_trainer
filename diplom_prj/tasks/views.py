from django.shortcuts import render, HttpResponse

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
      tasks_str = '\', \''.join(tasks_arr)
      if get_turple['language'] != 'All':
        tasks = Tasks.objects.raw('SELECT * FROM public.tasks_tasks WHERE name IN (\'' + tasks_str + '\') ORDER BY id ASC')

    if request.GET.get('tag', False):
      tasks_arr = []
      for task in tasks:
        tmp_arr = task.tags.split()
        for el in tmp_arr:
          if el == get_turple['tag']:
            tasks_arr.append(task.name)
      tasks_str = '\', \''.join(tasks_arr)
      tasks = Tasks.objects.raw('SELECT * FROM public.tasks_tasks WHERE name IN (\'' + tasks_str + '\') ORDER BY id ASC')

    print(tasks)

  
  return render(request, 'tasks/tasks.html', {
    'title' : 'Tasks',
    'tasks': tasks,
  })

def homepage(request):
  return render(request, 'tasks/homepage.html', {
    'title' : 'Homepage'
  })