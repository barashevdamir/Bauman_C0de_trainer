from django.contrib import admin
from django.db.models import Q

from . import models

@admin.register(models.Test)
class TestAdmin(admin.ModelAdmin):
    list_display = [
        'author', 
        'title', 
        'publish', 
        'prog_language', 
        'status'
    ]
    list_filter = [
        'status', 
        'created',
        'prog_language',
        'author' 
    ]
    search_fields = [
        'title',
        'author'
    ] #теги?
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

class AnswerInLine(admin.TabularInline):
    model = models.Answer

class TestQuestionFilter(admin.SimpleListFilter):
    title = 'test'
    parameter_name = 'test'

    def lookups(self, request, model_admin):  
        tests = models.Test.objects.all()
        lookups = ()
        for test in tests:
            lookups += ((test.title, test.title),)
            return lookups

    def queryset(self, request, queryset): 
        if self.value(): 
            test_title = self.value()
            return queryset.filter(Q(test__title=test_title))

@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
	fields = [
		'prompt',
		'test',
	]
	list_display=['id', 'prompt', 'test']
	list_filter=[TestQuestionFilter, ]
	search_fields=['test', 'title']
	inlines = [AnswerInLine, ]

class AnswerQuestionFilter(admin.SimpleListFilter):
	title = 'test'
	parameter_name = 'test'

	def lookups(self, request, model_admin): 
		tests = models.Test.objects.all()
		lookups = ()
		for test in tests:
			lookups += ((test.title, test.title),)
		return lookups

	def queryset(self, request, queryset): 
		if self.value(): 
			test_title = self.value()
			return queryset.filter(Q(question__test__title=test_title))

@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
	list_display=['text', 'correct', 'question']
	list_filter=[AnswerQuestionFilter, ]