from django.urls import path

from .views import *

urlpatterns = [
  path('', taskspage, name='tasks'),
  # path('<int:id>/', csrf_protect(index), name='training'), как было в training
  path('task-id<int:id>/', task, name='task'),
  # path('compile/', compile_code, name='compile-code'), как было в training

  # # path('runcode/', csrf_protect(runcode), name='runcode'),
  
  # path('<int:id>/compilator/', compilator, name='compilator'), как было в training
]
