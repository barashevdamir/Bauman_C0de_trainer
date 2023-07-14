from django.shortcuts import render
from django.contrib.auth.models import User
from tasks.models import Result as taskResult, Tasks
from tests.models import Result as testResult, Test
from diplom.choices_classes import Status
from django.utils import timezone
from django.db.models import Sum
from operator import itemgetter
import datetime 

def homepage(request):
  return render(request, 'home/homepage.html')

def leaderboard(request):
  if request.GET and request.headers.get('x-requested-with') == 'XMLHttpRequest':
    total_tasks_count = Tasks.objects.filter(status=Status.PUBLISHED).count()
    total_tests_count = Test.objects.filter(status=Status.PUBLISHED).count()
    tasksResult = taskResult.objects.filter(passed=True).values('user', 'task', 'exp_gain', 'date').distinct()
    testsResult = testResult.objects.filter(passed=True).values('user', 'test', 'exp_gain', 'date').distinct()
    if request.GET.get('exam') == 'tasks':
      testsResult = False
      total_tests_count = False
    if request.GET.get('exam') == 'tests':
      tasksResult = False
      total_tasks_count = False
    if request.GET.get('time') != 'all':
      if tasksResult:
        tasksResult = tasksResult.filter(date__gte = (timezone.now()-datetime.timedelta(days=int(request.GET.get('time')))))  
      if testsResult:
        testsResult = testsResult.filter(date__gte = (timezone.now()-datetime.timedelta(days=int(request.GET.get('time')))))
    if tasksResult:
      tasksResult = tasksResult.values('user').annotate(exp=Sum('exp_gain', distinct=True))
      total_tasks_count = Tasks.objects.filter(status=Status.PUBLISHED).count()
    if testsResult:
      testsResult = testsResult.values('user').annotate(exp=Sum('exp_gain', distinct=True))
      total_tests_count = Test.objects.filter(status=Status.PUBLISHED).count()
    users_list = []
    if tasksResult and testsResult:
      for element in list(tasksResult):
        try:
          add_exp=testsResult.get(user=element['user'])['exp']
          users_list.append({'user':element['user'], 'exp': element['exp']+add_exp})
        except testResult.DoesNotExist:
          users_list.append(element)
      for element in list(testsResult):
        try:
          tasksResult.get(user=element['user'])
        except taskResult.DoesNotExist: 
          users_list.append(element)
    elif tasksResult:
      users_list = list(tasksResult)
    elif testsResult:
      users_list = list(testsResult)
    users_list = sorted(users_list, key=itemgetter('exp'), reverse=True)[:50]
    for user in users_list:
      user['tests'] = testResult.objects.filter(user=user['user'], passed=True).values('test').distinct().count()
      user['tasks'] = taskResult.objects.filter(user=user['user'], passed=True).values('task').distinct().count()
      user['username'] = User.objects.get(id=user['user']).username
    return render(
    request, 
    'home/leaderboard_table.html',
      {
        'total_tasks_count': total_tasks_count,
        'total_tests_count': total_tests_count,
        'users_list': users_list,
      }
    )
  else:
    return render(
      request, 
      'home/leaderboard.html',
      {'load': 'leaderboard'}
    )