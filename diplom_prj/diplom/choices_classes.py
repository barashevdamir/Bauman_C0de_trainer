from django.db.models import TextChoices

class ProgLanguage(TextChoices):
    """
    This class needed to select languages in models

    When adding new languages, it's necessary that the first value 
    corresponds to the extension of the language files

    The second value should correspond to the usual readable form
    """
    
    # GENERAL = 'GEN', 'General'
    PYTHON = 'PY', 'Python'
    JAVASCRIPT = 'JS', 'JavaScript'
    HTML = 'HTML', 'HTML'
    SQL = 'SQL', 'SQL'
    PHP = 'PHP', 'PHP'

class Status(TextChoices):
    DRAFT = 'DF', 'Draft'
    PUBLISHED = 'PB', 'Published'

class AnswerType(TextChoices):
    SINGLE = 'SC', 'single choice'
    MULTIPLE = 'MC', 'multiple choice'
    WRITE = 'WR', 'write in'