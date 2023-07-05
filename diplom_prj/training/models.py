from django.db import models

# Create your models here.


class TaskSolution(models.Model):
    name = models.CharField(max_length=15)
    description = models.TextField()
    # solution =
    # test  =


def __str__(self):
    return self.name


