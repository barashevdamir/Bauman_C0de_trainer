from django import template
from tests.models import Test
from diplom.choices_classes import ProgLanguage, Status

register = template.Library()

@register.simple_tag
def get_prog_langs():
    langs_list = []
    used_langs_list = []
    used_langs_dict_list = list(Test.objects.filter(status=Status.PUBLISHED).values('prog_language').distinct())
    all_langs_list = ProgLanguage.choices
    for lang in used_langs_dict_list:
        used_langs_list.append(lang['prog_language'])
    for lang in all_langs_list:
        if lang[0] in used_langs_list:
            langs_list.append(lang)
    langs_list.sort()
    return langs_list

@register.simple_tag
def get_tests_tags():
    used_tags_ids_dict_list = list(Test.objects.filter(status=Status.PUBLISHED).values('tags').distinct())
    used_tags_ids = []
    for id in used_tags_ids_dict_list:
        used_tags_ids.append(id['tags'])
    used_tags_ids = set(used_tags_ids)
    tags_list = Test.tags.filter(id__in = used_tags_ids).order_by('name')
    return tags_list
