from django.urls import path

from .views import *

urlpatterns = [
    path('', test_list, name='tests'),
    path('test/', test, name='test'),
    path('tets/result', result, name='result')
]