import sys
import epicbox


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


# @csrf_protect
# def runcode(request, id):
#     data = TaskSolution.objects.get(id=id)
#     if request.method == "POST":
#         codeareadata = request.POST.get['codearea']
#         try:
#             # original_stdout = sys.stdout   #Запоминаем стандартный вывод
#             # sys.stdout = open('file.txt', 'w')  #Заменяем стандартный вывод на только что созданный файл
#             #
#             # exec(codeareadata)  #Выполняем код
#             #
#             # sys.stdout.close()
#             #
#             # sys.stdout = original_stdout  #Возвращаем стандартный вывод на свое место
#             #
#             # output = open('file.txt', 'r').read()  #Считываем итог из файла
#             result = subprocess.check_output(['python', '-c', codeareadata], universal_newlines=True, stderr=subprocess.STDOUT)
#             return JsonResponse({'result': result})
#
#         except subprocess.CalledProcessError as e:
#             return JsonResponse({'result': 'Error: ' + str(e.output)})
#         # except Exception as e:
#         #     sys.stdout = original_stdout
#         #     output = e
#
#     #В конце концов возвращаем результат
#     return render(request, './training/training.html', {'id': id})   #{'code': codeareadata, 'output': output})





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
        result = epicbox.run('python', 'python3 main.py', files=files, limits=limits)
        print(result)
        return render(request, './training/training.html', {'id': id})

    elif language == "node":
        pass

    elif language == "c":
        pass

    elif language == "cpp":
        pass

