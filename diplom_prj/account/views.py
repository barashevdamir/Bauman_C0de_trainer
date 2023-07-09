from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, \
    UserEditForm, ProfileEditForm, UpdateUserForm, UpdateProfileForm
from .models import Profile
from tasks.models import Result, Tasks, TaskLanguage
from tests.models import Result as testResult
from tests.models import Test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django_ratelimit.decorators import ratelimit
from diplom.choices_classes import ProgLanguage, Status

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {
                                                    'title': 'userLogin',
                                                    'navbar': True,
                                                    'form': form,
                                                  })

def register(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(request.POST)

            # Placeholder for actual validation logic
        if len(username) < 4 or len(password) < 6:
            return JsonResponse({'valid': False,
                                     'error': 'Username must be at least 4 characters and password at least 6 characters long.'})
        else:
                # Check if user exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({'valid': False, 'error': 'Username already exists.'})

        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
                # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
                # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
                # Save the User object
            new_user.save()
                # Create the user profile
            Profile.objects.create(user=new_user)
            return JsonResponse({'valid': True})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {
                      'title': 'Register',
                      'navbar': True,
                      'user_form': user_form,
                  })


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated '\
                                      'successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile)

    context = {
        'title': 'profileEdit',
        'navbar': True,
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'account/edit.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    # Дополнительный контекст для подсчета задач

    passed_tasks_count_langs = {}

    for lang in ProgLanguage.values:
        total_tasks_quantity = TaskLanguage.objects.filter(prog_language=lang).count()
        passed_tasks_count_quantity = Result.objects.filter(user=request.user, passed=True, prog_language=lang).values('task').distinct().count()
        if total_tasks_quantity == 0:
            tasks_progress = 0
        else:
            tasks_progress = int(100*passed_tasks_count_quantity/total_tasks_quantity)
        passed_tasks_count_langs[lang] = tasks_progress
    passed_tasks_count = Result.objects.filter(user=request.user, passed=True).values('task').distinct().count()
    total_tasks_count = Tasks.objects.filter(status=Status.PUBLISHED).count()
    passed_tasks_count_langs['total'] = int(100*(passed_tasks_count/total_tasks_count))

    passed_tests_count = testResult.objects.filter(user=request.user, passed=True).values('test').distinct().count()
    total_tests_count = Test.objects.filter(status=Status.PUBLISHED).count()
    tests_progress = int(100*passed_tests_count/total_tests_count)


    return render(request, 'account/user_profile.html', {
                                                        'title': 'Profile',
                                                        'navbar': True,
                                                        'user_form': user_form,
                                                        'profile_form': profile_form,
                                                        'passed_tasks_count': passed_tasks_count,
                                                        'total_tasks_count': total_tasks_count,
                                                        'passed_tasks_count_langs': passed_tasks_count_langs,
                                                        'passed_tests_count': passed_tests_count,
                                                        'total_tests_count': total_tests_count,
                                                        'tests_progress': tests_progress,
    })


def logout_user(request):
    logout(request)
    return redirect('login')

def sample_view(request):
    current_user = request.user
    return current_user.id


@ratelimit(key='ip', rate='10/m')
def validate_email(request):
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        return JsonResponse({'message': 'Too many requests'}, status=429)

    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)


@ratelimit(key='ip', rate='10/m')
def validate_username(request):
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        return JsonResponse({'message': 'Too many requests'}, status=429)

    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


