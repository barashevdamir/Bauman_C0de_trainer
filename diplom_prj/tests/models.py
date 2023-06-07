from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator
from taggit.managers import TaggableManager 

class Test(models.Model):
	
	class ProgLanguage(models.TextChoices):
		PYTHON = 'PY', 'Python'
		JAVASCRIPT = 'JS', 'JavaScript'
		HTML = 'HTML', 'HTML'
		SQL = 'SQL', 'SQL'
	
	class Status(models.TextChoices):
		DRAFT = 'DF', 'Draft'
		PUBLISHED = 'PB', 'Published'
		TESTING = 'TE', 'Testing'

	author = models.ForeignKey(
		User, 
		on_delete=models.SET_DEFAULT, 
		default=None,
		related_name='tests'
	)
	title = models.CharField(max_length=256, default='')
	slug = models.CharField(max_length=256, default='')
	times_taken = models.IntegerField(default=0, editable=False)
	experience = models.PositiveSmallIntegerField( #эквивалетнт lvl в задачках, нужно для таблицы лидеров, хотя может тесты и не достойны там учитываться
		default=1, 
		validators=[MaxValueValidator(limit_value=10)]
	) 
	prog_language = models.CharField(
		'Programming language',
		max_length=4,
		choices=ProgLanguage.choices,
		default=ProgLanguage.PYTHON, #может нужен пустой выбор?
		blank=False
	)
	tags = TaggableManager()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(
		'Test status',
		max_length=2,
		choices=Status.choices,
		default=Status.DRAFT,
		blank=False
	)

	@property
	def question_count(self):
		return self.questions.count()
	
	class Meta:
		verbose_name_plural = "Tests"
		ordering = ['-publish']
		indexes = [
			models.Index(fields=['-publish'])
		]

	def __str__(self):
		return self.title

class Question(models.Model):
	
	class AnswerType(models.TextChoices):
		SINGLE = 'SC', 'single choice'
		MULTIPLE = 'MC', 'multiple choice'
		WRITE = 'WR', 'write in'
	
	test = models.ForeignKey(
		Test, 
		related_name='questions', 
		on_delete=models.CASCADE
	)
	prompt = models.CharField(max_length=256, default='')
	answer_type = models.CharField(
        'Answer type',
		max_length=2,
        choices=AnswerType.choices,
        default=AnswerType.SINGLE,
		blank=False
    )

	@property
	def answer_count(self):
		return self.answers.count()
	
	class Meta:
		verbose_name_plural = "Questions"
		ordering = ['id']

	def __str__(self):
		return f'{self.prompt}, {self.answer_type}'

class Answer(models.Model):
	question = models.ForeignKey(
		Question, 
		related_name='answers', 
		on_delete=models.CASCADE
	)
	text = models.CharField(max_length=128)
	correct = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = "Answers"
		ordering = ['question']

	def __str__(self):
		return f'{self.text}, {self.correct}'
	
class Code(models.Model):
	question = models.ForeignKey(
		Question, 
		related_name='codes', 
		on_delete=models.CASCADE
	)
	text = models.TextField(help_text='can use markdown')

	class Meta:
		verbose_name_plural = "Codes"
		ordering = ['question']

	def __str__(self):
		return self.text[:20]