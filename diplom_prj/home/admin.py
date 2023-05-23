from django.contrib import admin

# Register your models here.
from .models import *

class TasksAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'create_datetime']
  list_display_links = ['id', 'name']
  search_fields = ['name']

admin.site.register(Tasks, TasksAdmin)