from django.urls import path

from .views import *

urlpatterns = [
    path('', tests, name='tests')
]