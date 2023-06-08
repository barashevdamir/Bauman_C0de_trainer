from django.urls import path, include
from .views import *
from django.views.decorators.csrf import csrf_protect

urlpatterns = [
    path('', csrf_protect(index), name='training'),
    path('runcode/', csrf_protect(runcode), name='runcode'),
]