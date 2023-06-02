from django.contrib import admin


from . import models

# не работали поля поиска, нужно разобраться и восстановить их

# описанный ниже код будет выдвать ошибку, 
# если один и тот же объект будут менять два человека
# возможно стоит поискать способ решения этой проблемы

class AnswerInLine(admin.TabularInline):
    extra = 1
    model = models.Answer
    
@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_filter = [
        'answer_type',
        'test'
    ]
    inlines = [AnswerInLine]

class QuestionInLine(admin.TabularInline):
    extra = 1
    model = models.Question
       
@admin.register(models.Test)
class TestAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'author',
        'prog_language', 
        'publish',
        'status'
    ]
    list_filter = [
        'status', 
        'prog_language',
        'created',
        'author' 
    ]
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    inlines = [QuestionInLine]


