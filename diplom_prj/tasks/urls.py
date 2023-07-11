from django.urls import path
from . import views
from .views import *

urlpatterns = [
  path('', taskspage, name='tasks'),
  path('task-id<int:id>/', task, name='task'),
  path('get_solution/', views.get_solution, name='get_solution'),
]
