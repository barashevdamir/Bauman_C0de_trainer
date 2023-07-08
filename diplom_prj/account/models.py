from django.db import models
from django.conf import settings
from PIL import Image
from tasks.models import Result, Tasks

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

    def passed_tasks_count(self):
        return Result.objects.filter(user=self.user, passed=True).count()

    def total_tasks_count(self):
        return Tasks.objects.all().count()

    def __str__(self):
        return f'Profile of {self.user.username}'

