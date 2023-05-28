from django.db import models

# Create your models here.
class Tasks(models.Model):
  name=models.CharField(max_length=160)
  create_datetime=models.DateTimeField(auto_now_add=True)
  positive_rate=models.PositiveSmallIntegerField(default=0)
  rate_count=models.PositiveSmallIntegerField(default=0)
  solved=models.PositiveIntegerField(default=0)
  level=models.PositiveSmallIntegerField(null=True)
  tags=models.TextField(null=True)
  languages=models.TextField(null=True)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = 'Tasks'
    verbose_name_plural = 'Tasks'
    ordering = ['create_datetime']