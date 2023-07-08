from django.urls import path

from .views import *

urlpatterns = [
  path('', taskspage, name='tasks'),
  path('task-id<int:id>/', task, name='task'),
  path('task-id<int:id>/check', task_check, name='task_check'),
]
