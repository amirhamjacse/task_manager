from django.db import models
from django.contrib.auth import get_user_model
from task_manager.abstract_model import AbsTimeMixin

User = get_user_model()


class Task(AbsTimeMixin):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    title = models.CharField(
        max_length=255, 
        null=True, blank=True
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    due_date = models.DateField(
        blank=True, null=True
    )
    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES
    )
    is_complete = models.BooleanField(
        default=False
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.title}'


class Photos(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE,
        related_name='task'
    )
    image = models.ImageField(
        upload_to='media/task_photos/'
    )
    description = models.TextField(
        blank=True, null=True
    )

    # def __str__(self):
    #     return self.description
