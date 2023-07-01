from django import template
from tests.models import Test

register = template.Library()

@register.simple_tag
def get_prog_langs():
    langs_list = Test.ProgLanguage.choices
    langs_list.sort()
    return langs_list

@register.simple_tag
def get_tests_tags():
    tags_list = Test.tags.order_by('name')
    return tags_list
