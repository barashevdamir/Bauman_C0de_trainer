from django.core.files import File
from diplom.choices_classes import ProgLanguage
from django.conf import settings
import os
import epicbox

epicbox.configure(
    profiles=[
        epicbox.Profile(f'{ProgLanguage.PYTHON}', 'python'),
        epicbox.Profile(f'{ProgLanguage.JAVASCRIPT}', 'node'),
    ]
)

def create_file(task, user, code, language):
    directory = 'results/{0}_id{1}/{2}_id{3}'.format(user.username, user.id, task.slug, task.id)
    file_name = directory + f'/{task.slug}-id{task.id}.{str.lower(language)}'
    if not os.path.exists(f"{settings.MEDIA_ROOT}/{directory}"):
        os.makedirs(f"{settings.MEDIA_ROOT}/{directory}")
    with open(f"{settings.MEDIA_ROOT}/{file_name}", "w") as file:
        code_file = File(file, name=file_name)
        code_file.write(code)  
    return code_file

def get_epic_code(code, language, test_code=None):
    if test_code == None:
        epic_code = bytes(code, 'utf-8')
    else:
        if language == ProgLanguage.PYTHON:
            epic_code = bytes(code, 'utf-8') + b'\n\n' + test_code
        elif language == ProgLanguage.JAVASCRIPT:
            epic_code = b'''const assert = require('assert');''' + b'\n\n' + bytes(code, 'utf-8') + b'\n\n' + test_code
    return epic_code

def run_epic_code(epic_code, language, cputime=1, memory=64):
    files = [{'name': f'epic_code.{str.lower(language)}', 'content': epic_code}]
    limits = {'cputime': cputime, 'memory': memory}
    if language == ProgLanguage.PYTHON:
        epic_command = 'python3 -m unittest epic_code.py'
    elif language == ProgLanguage.JAVASCRIPT:
        epic_command = 'node epic_code.js'
    result = epicbox.run(
        language, 
        epic_command,
        files=files,
        limits=limits
    )
    return result

def check_result(result, lvl):
    check = {}
    duration = result['duration']
    timeout = result['timeout']
    oom_killed = result['oom_killed']
    out = result['stdout'] + result['stderr']
    if result['exit_code'] == 0:
        passed = True
        exp_gain = lvl*3
        out = result['stdout']
        testing = "Tests passed successfully."
    else:
        passed = False
        exp_gain = 0
        out = result['stderr']
        testing = "Tests failed."
    message = f'{testing} Duration: {duration}. Timeout: {timeout}. OOM killed: {oom_killed}'
    check['passed'] = passed
    check['exp_gain'] = exp_gain
    check['message'] = message #+ '\n' + out.decode()
    check['out'] = out.decode()
    return check