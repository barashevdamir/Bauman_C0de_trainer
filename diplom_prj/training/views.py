import sys
import os
import epicbox
import tempfile
import shutil
import pytest

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import TaskSolution
import subprocess

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt


# @csrf_exempt
# def execute_code(request):
#     if request.method == 'POST':
#         code = request.POST.get('code')  # Получаем код из тела запроса
#
#         # Выполняем компиляцию и выполнение кода
#         try:
#             exec(code)
#             result = "Code executed successfully."
#         except Exception as e:
#             result = f"An error occurred: {str(e)}"
#
#         return JsonResponse({'result': result})
#
#     return JsonResponse({'error': 'Invalid request method'})

@csrf_protect
def index(request, id):
    try:
        data = TaskSolution.objects.get(id=id)
        return render(request, './training/training.html', {'data': data})
    except TaskSolution.DoesNotExist:
        return render(request, './training/training.html', {'error': 'Запись не найдена'})

@csrf_exempt
def compile_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            # Компиляция кода
            # Ваш код для компиляции
            result = subprocess.check_output(
                ['python', '-m', 'compileall', '-f', '-q', '-x', '__pycache__', '-o', '/dev/null', '-'],
                input=code.encode(), universal_newlines=True, stderr=subprocess.STDOUT)

            return JsonResponse({'result': result})
        except subprocess.CalledProcessError as e:
            return JsonResponse({'result': 'Error: ' + str(e.output)})
    return render(request, './training/compile_code.html')


def compilator(request, id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        datas = dict(request.POST.lists())

        language = str.lower(datas['language'][0])

        code = datas['code'][0]
        if language =='python':
            file_path = "media/temp/" + str(id) + ".py"
            program_file = open(file_path, "w")
            program_file.write(code)
            program_file.close()

    if language == "php":
        pass

    elif language == "python":

        epicbox.configure(
            profiles=[
                epicbox.Profile('python', 'python')
            ]
        )

        files = [{'name': 'main.py', 'content': bytes(code, 'utf-8')}]
        limits = {'cputime': 1, 'memory': 64}
        output = epicbox.run('python', 'python3 main.py', files=files, limits=limits)
        print(output)

        temp_dir = tempfile.mkdtemp()

        test_code = """
        import pytest

        def test_example():
            assert 2 + 2 == 4
        """

        epicbox.configure(profiles=[
            epicbox.Profile('python', 'python:latest')
        ])

        files = [{'name': 'test_code.py', 'content': bytes(test_code, 'utf-8')}]
        limits = {'cputime': 1, 'memory': 128}

        container = epicbox.run('python', 'python3 -m test_code.py',
                                files=files,
                                limits=limits)

        stdout_path = os.path.join(temp_dir, 'stdout')
        stderr_path = os.path.join(temp_dir, 'stderr')

        with open(stdout_path, 'wb') as stdout_file:
            stdout_file.write(container['stdout'])

        with open(stderr_path, 'wb') as stderr_file:
            stderr_file.write(container['stderr'])

        if container['exit_code'] == 0:
            print("Тесты пройдены успешно.")
        else:
            print("Тесты провалены.")

        shutil.rmtree(temp_dir)

        return render(request, './training/training.html', {'id': id, 'code': code, 'output': output})

    elif language == "node":
        pass

    elif language == "c":
        pass

    elif language == "cpp":
        pass

