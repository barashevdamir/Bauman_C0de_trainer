from django.urls import path

from .views import *

urlpatterns = [
    path('', test_list, name='tests_list'),
    path('test-id<int:id>/', test, name='test'),
    path('test-id<int:id>/save/', save_result, name='save_result'),
    path('test-id<int:id>/result/', result, name='result'),
]