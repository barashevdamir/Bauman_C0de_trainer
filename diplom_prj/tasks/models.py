from django.db import models
from django.contrib.auth.models import User
from django.db.models.constraints import UniqueConstraint
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
    blank=True,
		related_name='tasks'
	)
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
  tags = TaggableManager()
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

  def languages_count(self):
    return self.languages.count()

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

def tasks_solution_directory_path(instance, filename):
  task = Tasks.objects.get(id=instance.task.id)
  # file will be uploaded to MEDIA_ROOT/tasks_tests/<task.slug>_<task.id>/<filename>
  return 'tasks_solution/{0}_id{1}/{2}'.format(task.slug, task.id, filename)

def user_tasks_result_directory_path(instance, filename):
  user = User.objects.get(id=instance.user.id)
  task = Tasks.objects.get(id=instance.task.id)
  # file will be uploaded to MEDIA_ROOT/results/<user.username>_<user.id>/<task.slug>_<task.id>/<filename>
  return 'results/{0}_id{1}/{2}_id{3}/{4}'.format(user.username, user.id, task.slug, task.id, filename)

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
  solution_file = models.FileField(
      null=True,
      blank=True,
      default=None,
      upload_to=tasks_solution_directory_path
  )
  class Meta:
    constraints = (
      UniqueConstraint(
        fields=['task', 'prog_language'],
        name='unique_language',
      ),
    )


class Result(models.Model):
  user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
    related_name='task_result'
	)
  task = models.ForeignKey(
		Tasks,
		on_delete=models.CASCADE
	)
  passed = models.BooleanField(default=False)
  exp_gain = models.PositiveSmallIntegerField(default=0)
  prog_language = models.CharField(
    'Programming language',
    max_length=4,
    choices=ProgLanguage.choices,
    default=None,
    blank=True
  )
  # version = models.CharField(max_length=50)
  result_code = models.FileField(
    null=True,
    blank=True,
    default=None,
    upload_to=user_tasks_result_directory_path
  )
  date = models.DateTimeField(default=timezone.now)
  code = models.TextField()
  file_name = models.CharField(max_length=100)
  result = models.TextField(blank=True, null=True)

  def __str__(self):
	  return f'{self.user} gain {self.exp_gain} experience after passing {self.task}. Date: {self.date}'


