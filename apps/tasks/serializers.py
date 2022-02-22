from rest_framework import serializers

from apps.comments.serializers import CommentSerializer
from apps.tasks.models import Task, Timelog


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title')


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description', 'completed')


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'completed')


class TaskItemSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'completed', 'owner', 'comments')


class TimeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timelog
        fields = '__all__'
        # extra_kwargs = {
        #     'task': {'read_only': True},
        #     'start': {'read_only': True},
        #     'stop': {'read_only': True},
        #     'owner': {'read_only': True},
        # }
