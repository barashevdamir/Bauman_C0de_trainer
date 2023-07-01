# Generated by Django 4.2.1 on 2023-07-01 17:25

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('tasks', '0002_alter_tasks_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='task_tag',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
