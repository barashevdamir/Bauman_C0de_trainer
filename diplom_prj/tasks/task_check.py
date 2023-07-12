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
    file_name = f'{task.slug}-id{task.id}.{str.lower(language)}'
    directory = '{0}/results/{1}_id{2}/{3}_id{4}'.format(settings.MEDIA_ROOT, user.username, user.id, task.slug, task.id)
    # file_path = file_name + directory
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(f"{directory}/{file_name}", "w") as file:
        file.write(code)
    return file_name

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
    check['message'] = message
    check['out'] = out.decode()
    return check