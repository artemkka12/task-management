from django.shortcuts import get_object_or_404
from drf_util.decorators import serialize_decorator
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.tasks.models import Task
from apps.tasks.serializers import TaskCreateSerializer, TaskLIstSerializer, TaskItemSerializer


class TaskCreateView(GenericAPIView):
    serializer_class = TaskCreateSerializer

    permission_classes = (IsAuthenticated,)

    @serialize_decorator(TaskCreateSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        task = Task.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            completed=validated_data['completed'],
            owner=request.user,
        )

        task.save()

        return Response(task.pk)


class TaskListView(GenericAPIView):
    serializer_class = TaskLIstSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        tasks = Task.objects.all()

        return Response(TaskLIstSerializer(tasks, many=True).data)


class TaskItemView(GenericAPIView):
    serializer_class = TaskItemSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)

        return Response(TaskItemSerializer(task).data)
