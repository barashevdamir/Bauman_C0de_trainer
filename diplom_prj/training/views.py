import sys

from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import TaskSolution

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
def index(request):
    data = TaskSolution.objects.all()
    return render(request, './training/training.html', {'data': data})


@csrf_protect
def runcode(request):

    if request.method == "POST":
        codeareadata = request.POST['codearea']

        try:
            original_stdout = sys.stdout   #Запоминаем стандартный вывод
            sys.stdout = open('file.txt', 'w')  #Заменяем стандартный вывод на только что созданный файл

            exec(codeareadata)  #Выполняем код

            sys.stdout.close()

            sys.stdout = original_stdout  #Возвращаем стандартный вывод на свое место

            output = open('file.txt', 'r').read()  #Считываем итог из файла
        except Exception as e:
            sys.stdout = original_stdout
            output = e

    #В конце концов возвращаем результат
    return render(request, './training/training.html', {'code': codeareadata, 'output': output})
