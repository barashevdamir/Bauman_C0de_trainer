from django import template
from tasks.models import Tasks, TaskLanguage
from diplom.choices_classes import ProgLanguage, Status

register = template.Library()

@register.simple_tag()
def get_unique_languages():
  used_langs_ids_dict_list = list(Tasks.objects.filter(status=Status.PUBLISHED).values('languages').distinct())
  used_langs_ids_list = []
  for lang in used_langs_ids_dict_list:
    used_langs_ids_list.append(lang['languages'])
  langs_list = []
  used_langs_list = []
  used_langs_dict_list = list(TaskLanguage.objects.filter(id__in=used_langs_ids_list).values('prog_language').distinct())
  all_langs_list = ProgLanguage.choices
  for lang in used_langs_dict_list:
    used_langs_list.append(lang['prog_language'])
  for lang in all_langs_list:
    if lang[0] in used_langs_list:
      langs_list.append(lang)
  langs_list.sort()
  return langs_list

@register.simple_tag
def get_tasks_tags():
  used_tags_ids_dict_list = list(Tasks.objects.filter(status=Status.PUBLISHED).values('tags').distinct())
  used_tags_ids = []
  for id in used_tags_ids_dict_list:
    used_tags_ids.append(id['tags'])
  used_tags_ids = set(used_tags_ids)
  tags_list = Tasks.tags.filter(id__in = used_tags_ids).order_by('name')
  return tags_list


