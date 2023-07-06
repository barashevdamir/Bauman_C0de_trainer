from django.db.models import TextChoices

class ProgLanguage(TextChoices):
    # GENERAL = 'GEN', 'General' для общих вопросов по программированию, нужно ли?
    PYTHON = 'PY', 'Python'
    JAVASCRIPT = 'JS', 'JavaScript'
    HTML = 'HTML', 'HTML'
    SQL = 'SQL', 'SQL'

class Status(TextChoices):
    DRAFT = 'DF', 'Draft'
    PUBLISHED = 'PB', 'Published'

class AnswerType(TextChoices):
    SINGLE = 'SC', 'single choice'
    MULTIPLE = 'MC', 'multiple choice'
    WRITE = 'WR', 'write in'