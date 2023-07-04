from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator
from taggit.managers import TaggableManager 

class Test(models.Model):
	
	class ProgLanguage(models.TextChoices):
		# GENERAL = 'GEN', 'General' для общих вопросов по программированию, нужно ли?
		PYTHON = 'PY', 'Python'
		JAVASCRIPT = 'JS', 'JavaScript'
		HTML = 'HTML', 'HTML'
		SQL = 'SQL', 'SQL'
	
	class Status(models.TextChoices):
		DRAFT = 'DF', 'Draft'
		PUBLISHED = 'PB', 'Published'

	author = models.ForeignKey(
		User, 
		on_delete=models.SET_DEFAULT, 
		default=None,
		related_name='tests'
	)
	title = models.CharField(max_length=256, default='')
	slug = models.CharField(max_length=256, default='')
	score_to_pass = models.PositiveSmallIntegerField(
		'Required score to pass',
		help_text='score in percentages',
		default=80, 
		validators=[MaxValueValidator(limit_value=100)]
	)
	# times_taken = models.PositiveIntegerField(default=0, editable=False)
	experience = models.PositiveSmallIntegerField( #эквивалетнт lvl в задачках, нужно для таблицы лидеров, хотя может тесты и не достойны там учитываться
		default=1, 
		validators=[MaxValueValidator(limit_value=3)]
	) 
	prog_language = models.CharField(
		'Programming language',
		max_length=4,
		choices=ProgLanguage.choices,
		default=ProgLanguage.PYTHON,
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

	def question_count(self):
		return self.questions.count()
	
	def get_questions(self):
		return self.questions.all()
	
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
		on_delete=models.CASCADE,
		related_name='questions'
	)
	prompt = models.CharField(max_length=256, default='')
	answer_type = models.CharField(
        'Answer type',
		max_length=2,
        choices=AnswerType.choices,
        default=AnswerType.SINGLE,
		blank=False
    )

	def answer_count(self):
		return self.answers.count()
	
	def get_answers(self):
		return self.answers.all()
	
	def get_correct_answers(self):
		return self.answers.filter(correct=True)
	
	def get_codes(self):
		return self.codes.all()

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
		return f'{self.text} Correct: {self.correct}'
	
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
	
class Result(models.Model):
	user = models.ForeignKey(
		User, 
		on_delete=models.CASCADE, 
		related_name='test_result'
	)
	test = models.ForeignKey(
		Test,  
		on_delete=models.CASCADE
	)
	passed = models.BooleanField(default=False)
	score = models.PositiveSmallIntegerField(default=0)
	exp_gain = models.PositiveSmallIntegerField(default=0)
	pass_date = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name_plural = "Results"
		ordering = ['user']

	def __str__(self):
		return f'{self.user} gain {self.exp_gain} experience after passing {self.test}'