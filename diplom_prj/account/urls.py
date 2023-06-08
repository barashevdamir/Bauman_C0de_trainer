from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import logout_user
from django.contrib.auth.views import PasswordChangeView


urlpatterns = [

    # path('login/', views.user_login, name='login'),

    # path('login/', auth_views.LoginView.as_view(), name='login'),

    #
    # path('', views.dashboard, name='dashboard'),
    #
    # # change password urls
    # path('password-change/',
    #      auth_views.PasswordChangeView.as_view(success_url='password_change_done'),
    #      name='password_change'),
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('change_password/', PasswordChangeView.as_view(template_name='account/password_change_form'),
         name='password_change'),
    # #
    # # # reset password urls
    # path('password-reset/',
    #      auth_views.PasswordResetView.as_view(),
    #      name='password_reset'),
    # path('password-reset/done/',
    #      auth_views.PasswordResetDoneView.as_view(),
    #      name='password_reset_done'),
    # path('password-reset/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(),
    #      name='password_reset_confirm'),
    # path('password-reset/complete/',
    #      auth_views.PasswordResetCompleteView.as_view(),
    #      name='password_reset_complete'),
    path('logout/', logout_user, name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('profile/', views.profile, name='user_profile'),
]
