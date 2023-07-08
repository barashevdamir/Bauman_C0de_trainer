import os
from django.conf import settings
import epicbox
import tempfile
import shutil

def create_file(task, user, code, language):
    file_name = f'{task.slug}-{task.id}.{str.lower(language)}'
    directory = '{0}/results/{1}_id{2}/{3}_id{4}'.format(settings.MEDIA_ROOT, user.username, user.id, task.slug, task.id)
    # file_path = file_name + directory
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(f"{directory}/{file_name}", "w") as file:
        file.write(code)
    # return {'file_path': file_path, 'code': code}

def check_solution(code, language, test_file_path=None):
    if test_file_path == None:
        pass
    else:
        pass
