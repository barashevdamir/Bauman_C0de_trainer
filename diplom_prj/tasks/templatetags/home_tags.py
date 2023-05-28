from django import template
from tasks.models import *

register = template.Library()

@register.simple_tag()
def get_rate_procent(positive_rate, rate_count):
  if rate_count != 0:
    rate_procent = round(positive_rate/rate_count*100)
  return rate_procent

@register.simple_tag()
def get_array(list):
  return list.split('\n')

@register.simple_tag()
def get_unique_languages():
  tasks = Tasks.objects.all()
  lang_arr = ['All', ]
  for task in tasks:
    lang_arr += task.languages.split()
    lang_arr = list(set(lang_arr))
  return sorted(lang_arr)

@register.simple_tag()
def get_unique_tags():
  tasks = Tasks.objects.all()
  tag_arr = []
  for task in tasks:
    tag_arr += task.tags.split()
    tag_arr = list(set(tag_arr))
  return sorted(tag_arr)


