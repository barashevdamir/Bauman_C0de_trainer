from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import logout_user
from django.contrib.auth.views import PasswordChangeView


urlpatterns = [

    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('change_password/', PasswordChangeView.as_view(template_name='account/password_change_form'),
         name='password_change'),

    path('logout/', logout_user, name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('profile/', views.profile, name='user_profile'),
]
