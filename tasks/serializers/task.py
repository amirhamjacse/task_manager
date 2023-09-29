from rest_framework import serializers
from tasks.models import Task, Photos  # Replace with the actual import path to your models


class PhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = '__all__' 


class TaskSerializer(serializers.ModelSerializer):
    photos = PhotosSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
