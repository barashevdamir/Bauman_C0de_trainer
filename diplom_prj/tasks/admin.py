from django.contrib import admin
from .models import *

class TestingInputInLine(admin.TabularInline):
  extra = 1
  model = TestingInput

class TaskLanguageInLine(admin.TabularInline):
  extra = 1
  model = TaskLanguage

@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
  inlines = [TaskLanguageInLine, TestingInputInLine]
  list_display = ['id', 'title', 'created', 'status']
  list_display_links = ['id', 'title']
  search_fields = ['title']
  prepopulated_fields = {'slug': ('title',)}
