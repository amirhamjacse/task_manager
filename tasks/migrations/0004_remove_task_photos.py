# Generated by Django 4.2.5 on 2023-09-29 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_task_due_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='photos',
        ),
    ]