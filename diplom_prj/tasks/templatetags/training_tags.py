from django import template
from django.utils.safestring import mark_safe
import markdown
from diplom.choices_classes import ProgLanguage, Status

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.simple_tag
def get_prog_langs():
  langs_list = ProgLanguage.choices
  langs_list.sort()
  return langs_list
