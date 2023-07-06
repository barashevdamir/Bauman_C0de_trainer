# пример из документации
# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return 'user_{0}/{1}'.format(instance.user.id, filename)

def tasks_tests_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/tasks_tests/<slug>_<id>/<filename>
    return 'tasks_tests/{0}_id{1}/{2}'.format(instance.slug, instance.id, filename)