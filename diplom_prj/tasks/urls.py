from django.urls import path
from . import views
from .views import *

urlpatterns = [
  path('', taskspage, name='tasks'),
  path('task-id<int:id>/', task, name='task'),
]
