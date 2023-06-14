from django import template
from tests.models import Test

register = template.Library()

@register.simple_tag
def get_prog_langs():
    langs_list = Test.ProgLanguage.labels
    langs_list.sort()
    return langs_list

# @register.simple_tag
# def get_tags():
#     lang_list = Test.prog_language.labels
#     return lang_list