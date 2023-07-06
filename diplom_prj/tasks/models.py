from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from taggit.managers import TaggableManager 
from diplom.choices_classes import Status 

class Tasks(models.Model):
  
  # class Status(models.TextChoices):
  #   DRAFT = 'DF', 'Draft'
  #   PUBLISHED = 'PB', 'Published'

  
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
  level = models.PositiveSmallIntegerField(
    default=1,
    validators=[
      MinValueValidator(limit_value=1), 
      MaxValueValidator(limit_value=5)
    ],
  )
  languages = models.TextField(null=True) #плохой вариант, заменить
  tags = TaggableManager()
  test_file = models.FileField(null=True, blank=True, default=None) #ДОДЕЛАТЬ!!!!
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

# class Result(models.Model):
#   user = models.ForeignKey(
# 		User, 
# 		on_delete=models.CASCADE, 
# 		related_name='task_result'
# 	)
#   test = models.ForeignKey(
# 		Tasks,  
# 		on_delete=models.CASCADE
# 	)
