from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from drf_util.decorators import serialize_decorator
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet

from apps.tasks.models import Task, Timelog
from apps.tasks.serializers import (TaskCreateSerializer,
                                    TaskListSerializer,
                                    TaskItemSerializer, TaskSerializer, TimeLogSerializer)


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    @action(methods=['post'], detail=True, serializer_class=TaskSerializer)
    def complete_task(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        task = self.get_object()
        task = self.get_object()
        task.completed = True
        task.save()
        return Response({'status': 200})

    @action(methods=['post'], detail=True, serializer_class=Serializer)
    def start(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        task = self.get_object()
        user = request.user
        return Response('Done')


# class TaskCreateView(GenericAPIView):
#     serializer_class = TaskCreateSerializer
#
#     permission_classes = (IsAuthenticated,)
#
#     @serialize_decorator(TaskCreateSerializer)
#     def post(self, request):
#         validated_data = request.serializer.validated_data
#
#         task = Task.objects.create(
#             title=validated_data['title'],
#             description=validated_data['description'],
#             completed=validated_data['completed'],
#             owner=request.user,
#         )
#
#         task.save()
#
#         return Response(task.pk)


# class TaskListView(GenericAPIView):
#     serializer_class = TaskListSerializer
#     queryset = Task.objects.all()
#
#     permission_classes = (AllowAny,)
#
#     def get(self, request):
#         tasks = Task.objects.all()
#
#         return Response(TaskListSerializer(tasks, many=True).data)


# class TaskItemView(GenericAPIView):
#     serializer_class = TaskItemSerializer
#     queryset = Task.objects.all()
#     permission_classes = (AllowAny,)
#
#     def get(self, request, pk):
#         task = get_object_or_404(Task.objects.filter(pk=pk))
#
#         return Response(TaskItemSerializer(task).data)


# class MyTaskView(GenericAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request):
#         tasks = Task.objects.filter(owner_id=request.user.id)
#
#         return Response(TaskSerializer(tasks, many=True).data)
#
#
# class CompletedTaskView(GenericAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     permission_classes = (AllowAny,)
#
#     def get(self, request):
#         tasks = Task.objects.filter(completed=True)
#
#         return Response(TaskSerializer(tasks, many=True).data)
#
#
# class AssignTaskView(GenericAPIView):
#     queryset = Task.objects.all()
#
#     def patch(self, request, task_id, user_id):
#         task = get_object_or_404(Task.objects.filter(pk=task_id))
#         user = get_object_or_404(User.objects.filter(pk=user_id))
#         task.owner = user
#         task.save()
#
#         send_mail(
#             'Hello!',
#             'A task was assigned to you!'
#             , 'artemkka2280@gmail.com',
#             [user.email],
#         )
#
#         return Response(TaskItemSerializer(task).data)
#
#
# class CompleteTaskView(GenericAPIView):
#     queryset = Task.objects.all()
#
#     def patch(self, request, pk):
#         task = get_object_or_404(Task.objects.filter(pk=pk))
#         task.completed = True
#         task.save()
#
#         users = User.objects.filter(comments__task=task.pk).distinct()
#         for user in users:
#             print(user.email)
#             send_mail(
#                 'Hello!',
#                 'Task which you commented was completed!'
#                 , 'artemkka2280@gmail.com',
#                 [user.email],
#             )
#
#         return Response(TaskItemSerializer(task).data)
#
#
# class DeleteTaskView(GenericAPIView):
#     queryset = Task.objects.all()
#
#     def delete(self, request, pk):
#         task = get_object_or_404(Task.objects.filter(pk=pk))
#         task.delete()
#
#         return Response({'status': HTTP_200_OK})
#
#
# class SearchTaskView(GenericAPIView):
#     serializer_class = TaskSerializer
#     queryset = Task.objects.all()
#
#     def get(self, request, value):
#         tasks = Task.objects.filter(title__icontains=value)
#
#         return Response(TaskSerializer(tasks, many=True).data)


class StartLogTimeView(GenericAPIView):
    serializer_class = TimeLogSerializer
    queryset = Timelog.objects.all()

    @serialize_decorator(TimeLogSerializer)
    def post(self, request, pk):

        log = Timelog.objects.create(
            task=Task.objects.get(pk=pk),
            start=timezone.now(),
            stop=timezone.now()
        )

        log.save()

        return Response({'log id': log.pk})


class StopLogTimeView(GenericAPIView):
    serializer_class = TimeLogSerializer
    queryset = Timelog.objects.all()

    @serialize_decorator(TimeLogSerializer)
    def post(self, request, pk):

        log = Timelog.objects.filter(task_id=pk).last()
        log.stop = timezone.now()

        log.save()

        return Response({'spent time': log.stop - log.start})
