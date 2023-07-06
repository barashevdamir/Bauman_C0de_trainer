from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from taggit.managers import TaggableManager 
from diplom.choices_classes import Status, ProgLanguage 

class Tasks(models.Model):
  title = models.CharField(max_length=256, default='')
  slug = models.CharField(max_length=256, default='')
  author = models.ForeignKey(
		User, 
		on_delete=models.SET_DEFAULT, 
		default=None,
    null=True,
		related_name='tasks'
	)
  # positive_rate=models.PositiveSmallIntegerField(default=0)
  # rate_count=models.PositiveSmallIntegerField(default=0)
  # solved=models.PositiveIntegerField(default=0)
  description = models.TextField(
    default=None,
    null=True,
    blank=True
  )
  level = models.PositiveSmallIntegerField(
    default=1,
    validators=[
      MinValueValidator(limit_value=1), 
      MaxValueValidator(limit_value=5)
    ],
  )
  # languages = models.TextField(null=True) #плохой вариант, заменить
  tags = TaggableManager()
  # test_file = models.FileField(
  #   null=True, 
  #   blank=True, 
  #   default=None,
  #   upload_to=tasks_tests_directory_path
  #   ) # ВНИМАНИЕ!!! осбеность Django такова, что при очистке данного поля в модели файл не удаляется 
  #     # нужен специальный скрипт или удаление вручную
  publish = models.DateTimeField(default=timezone.now)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  status = models.CharField(
		'Task status',
		max_length=2,
		choices=Status.choices,
		default=Status.DRAFT,
		blank=False
	)

  def __str__(self):
    return self.title

  class Meta:
    verbose_name = 'Task'
    verbose_name_plural = 'Tasks'
    ordering = ['-publish']

class TestingInput(models.Model):
  task = models.ForeignKey(
    Tasks, 
		related_name='inputs', 
		on_delete=models.CASCADE
  )
  input_data = models.CharField(max_length=256, default='')
  expected_output = models.CharField(max_length=256, null=True, default=None)

def tasks_tests_directory_path(instance, filename):
  task = Tasks.objects.get(id=instance.task.id)
  # file will be uploaded to MEDIA_ROOT/tasks_tests/<task.slug>_<task.id>/<filename>
  return 'tasks_tests/{0}_id{1}/{2}'.format(task.slug, task.id, filename)

class TaskLanguage(models.Model):
  task = models.ForeignKey(
    Tasks, 
		related_name='languages', 
		on_delete=models.CASCADE
  )
  prog_language = models.CharField(
		'Programming language',
		max_length=4,
		choices=ProgLanguage.choices,
		default=None,
		blank=True
	)
  test_file = models.FileField(
    null=True, 
    blank=True, 
    default=None,
    upload_to=tasks_tests_directory_path
  )# ВНИМАНИЕ!!! осбеность Django такова, что при очистке данного поля в модели файл не удаляется 
   # нужен специальный скрипт или удаление вручную

# class Result(models.Model):
#   user = models.ForeignKey(
# 		User, 
# 		on_delete=models.CASCADE, 
# 		related_name='task_result'
# 	)
#   task = models.ForeignKey(
# 		Tasks,  
# 		on_delete=models.CASCADE
# 	)
