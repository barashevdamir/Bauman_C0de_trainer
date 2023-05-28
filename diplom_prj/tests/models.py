from django.db import models
from django.contrib.auth.models import User

class Test(models.Model):
	author = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None) #а нужно ли оно?
	title = models.CharField(max_length=256, default='') 
	created_at = models.DateTimeField(auto_now_add=True)
	times_taken = models.IntegerField(default=0, editable=False)
	experience = models.PositiveSmallIntegerField(default=0) #эвивалетнт lvl в задачках, нужно для таблицы лидеров, хотя может тесты и не достойны там учитываться
	prog_language = models.CharField(max_length=32, default='') #может сделать список для выбора языка? есть вариант сделать этот список общим для проекта и тащить его сюда и в модель задачек
	#может добавить описание?
	#теги?

	@property
	def question_count(self):
		return self.questions.count()
	
	class Meta:
		verbose_name_plural = "Tests"
		ordering = ['id']

	def __str__(self):
		return f'{self.title}, {self.author}'

class Question(models.Model):
	
	SINGLE = 'SC'
	MULTIPLE = 'MC'
	WRITTEN = 'WR'
	ANSWER_TYPE_CHOICES = [
		(SINGLE, 'single choice'),
		(MULTIPLE, 'multiple choice'),
		(WRITTEN,'written')
	]

	test = models.ForeignKey(
		Test, 
		related_name='questions', 
		on_delete=models.CASCADE
	)
	prompt = models.CharField(max_length=256, default='')
	answer_type = models.CharField(
        max_length=2,
        choices=ANSWER_TYPE_CHOICES,
        default=SINGLE,
		blank=False
    )
	#может нужна какая-то функция для проверки ответа соответсвию типу ответа?

	class Meta:
		verbose_name_plural = "Questions"
		ordering = ['id']

	def __str__(self):
		return F'{self.prompt}, {self.answer_type}'

class Answer(models.Model):
	question = models.ForeignKey(
		Question, 
		related_name='answers', 
		on_delete=models.CASCADE
	)
	text = models.CharField(max_length=128)
	correct = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.text}, {self.correct}'