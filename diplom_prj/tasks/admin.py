from django.contrib import admin

# Register your models here.
from .models import *

class TasksAdmin(admin.ModelAdmin):
  list_display = ['id', 'title', 'created', 'status']
  list_display_links = ['id', 'title']
  search_fields = ['title']
  prepopulated_fields = {'slug': ('title',)}

admin.site.register(Tasks, TasksAdmin)