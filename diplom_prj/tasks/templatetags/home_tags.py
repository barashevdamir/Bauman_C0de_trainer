from django import template
from tasks.models import Tasks
from diplom.choices_classes import ProgLanguage, Status

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
  tasks = Tasks.objects.filter(status=Status.PUBLISHED)
  lang_arr = []
  for task in tasks:
    lang_arr += task.languages.split()
    lang_arr = list(set(lang_arr))
  return sorted(lang_arr)

@register.simple_tag
def get_tasks_tags():
  used_tags_ids_dict_list = list(Tasks.objects.filter(status=Status.PUBLISHED).values('tags').distinct())
  used_tags_ids = []
  for id in used_tags_ids_dict_list:
    used_tags_ids.append(id['tags'])
  used_tags_ids = set(used_tags_ids)
  tags_list = Tasks.tags.filter(id__in = used_tags_ids).order_by('name')
  return tags_list


