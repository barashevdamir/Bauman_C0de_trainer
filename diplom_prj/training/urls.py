from django.urls import path, include
from .views import *
from django.views.decorators.csrf import csrf_protect

urlpatterns = [
    path('<int:id>/', csrf_protect(index), name='training'),
    # path('runcode/', csrf_protect(runcode), name='runcode'),


    path('compile/', compile_code, name='compile-code'),
]
