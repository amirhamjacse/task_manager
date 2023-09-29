from django.contrib import admin
from tasks import models

# Register your models here.


@admin.register(models.CustomUser)
class UserModelAdmin(admin.ModelAdmin):
    list_display = [
        'email',
        'username',
        'date_joined',
        'is_active',
        'is_staff',
    ]


@admin.register(models.Task)
class TaskModelAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'description',
        'due_date',
        'priority',
        'is_complete',
        'owner',
    ]
    ordering = ("priority",)
    # list_editable = [
    #     "title"
    # ]


@admin.register(models.Photos)
class PhotosModleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'task',
        'image',
    ]
    list_editable = [
        "image"
    ]
