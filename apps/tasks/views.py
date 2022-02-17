from django.contrib.auth.models import User
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from drf_util.decorators import serialize_decorator
from rest_framework.status import HTTP_200_OK

from apps.tasks.models import Task
from apps.tasks.serializers import (TaskCreateSerializer,
                                    TaskLIstSerializer,
                                    TaskItemSerializer, TaskSerializer)


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
        tasks = get_object_or_404(Task.objects.all())

        return Response(TaskLIstSerializer(tasks, many=True).data)


class TaskItemView(GenericAPIView):
    serializer_class = TaskItemSerializer
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        task = get_object_or_404(Task.objects.filter(pk=pk))

        return Response(TaskItemSerializer(task).data)


class MyTaskView(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        tasks = get_object_or_404(Task.objects.filter(owner_id=request.user.id))

        return Response(TaskSerializer(tasks, many=True).data)


class CompletedTaskView(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        tasks = get_object_or_404(Task.objects.filter(completed=True))

        return Response(TaskSerializer(tasks, many=True).data)


class AssignTaskView(GenericAPIView):

    def patch(self, request, task_id, user_id):
        task = Task.objects.get(pk=task_id)
        user = User.objects.get(pk=user_id)
        task.owner = user
        task.save()

        return Response(TaskItemSerializer(task).data)


class CompleteTaskView(GenericAPIView):

    def patch(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.completed = True
        task.save()

        return Response(TaskItemSerializer(task).data)


class DeleteTaskView(GenericAPIView):

    def delete(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.delete()

        return Response({'status': HTTP_200_OK})
