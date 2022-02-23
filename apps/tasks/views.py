from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer

from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet

from apps.tasks.models import Task, Timelog, Timer
from apps.tasks.serializers import (TaskSerializer, AssignTaskSerializer, ManualTimeLogSerializer)
from config.settings import EMAIL_HOST_USER


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        task = Task.objects.create(title=data['title'], description=data['description'], owner=user)
        task.save()
        return Response(TaskSerializer(task).data)

    @action(methods=['patch'], detail=True, serializer_class=TaskSerializer)
    def complete_task(self, request, *args, **kwargs):
        task = self.get_object()
        task.completed = True
        task.save()

        users = User.objects.filter(comments__task=task.pk).distinct()
        for user in users:
            send_mail(
                'Hello!',
                'Task which you commented was completed!'
                , EMAIL_HOST_USER,
                [user.email],
            )

        return Response({'status': HTTP_200_OK})

    @action(methods=['get'], detail=False, serializer_class=TaskSerializer)
    def view_my_tasks(self, request, *args, **kwargs):
        tasks = Task.objects.filter(owner=request.user)
        return Response(TaskSerializer(tasks, many=True).data)

    @action(methods=['get'], detail=False, serializer_class=TaskSerializer)
    def view_completed_tasks(self, request, *args, **kwargs):
        tasks = Task.objects.filter(completed=True)
        return Response(TaskSerializer(tasks, many=True).data)

    @action(methods=['patch'], detail=True, serializer_class=AssignTaskSerializer)
    def assign_task_to_user(self, request, *args, **kwargs):
        task = self.get_object()
        user = get_object_or_404(User.objects.filter(pk=request.data['owner']))
        task.owner = user
        task.save()

        send_mail(
                    'Hello!',
                    'A task was assigned to you!'
                    , EMAIL_HOST_USER,
                    [user.email],
                )

        return Response(TaskSerializer(task).data)

    @action(methods=['post'], detail=True, serializer_class=Serializer)
    def start_time_log(self, request, *args, **kwargs):
        task = self.get_object()
        user = request.user
        timer = Timer.objects.create(
            owner=user,
            task=task,
        )
        timer.save()
        timer.start()
        # log = Timelog.objects.filter(task=task).last()
        #
        # if log is not None and log.is_running is False:
        #     raise ValidationError('You cannot start task')
        # else:
        #     log = Timelog.objects.create(
        #         task=task,
        #         start=timezone.now(),
        #         stop=None,
        #         duration=None,
        #         is_running=True,
        #         owner=user
        #     )
        #
        #     log.save()

        return Response({'status': HTTP_200_OK})

    @action(methods=['post'], detail=True, serializer_class=Serializer)
    def pause_time_log(self, request, *args, **kwargs):
        task = self.get_object()
        user = request.user
        timer = Timer.objects.filter(
            owner=user,
            task=task,
        ).last()
        timer.pause()

        return Response({'status': HTTP_200_OK, 'time spent': timer.total_duration})

    @action(methods=['post'], detail=True, serializer_class=Serializer)
    def stop_time_log(self, request, *args, **kwargs):
        task = self.get_object()
        user = request.user
        timer = Timer.objects.filter(
            owner=user,
            task=task,
        ).last()
        timer.stop()

        return Response({'status': HTTP_200_OK, 'time spent': timer.total_duration})



    # @action(methods=['post'], detail=True, serializer_class=Serializer)
    # def stop_time_log(self, request, *args, **kwargs):
    #     task = self.get_object()
    #
    #     log = Timelog.objects.filter(task=task).last()
    #
    #     if log.is_running is False and log.stop is not None:
    #         raise ValidationError('You cannot stop task')
    #     else:
    #         log.stop = timezone.now()
    #         log.is_running = False
    #         log.duration = (log.stop - log.start).seconds / 60
    #         log.save()
    #
    #         return Response({'status': HTTP_200_OK, 'time spent': log.duration})
    #
    # @action(methods=['post'], detail=True, serializer_class=ManualTimeLogSerializer)
    # def manual_time_log(self, request, *args, **kwargs):
    #     task = self.get_object()
    #     user = request.user
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     validated_data = serializer.validated_data
    #     log = Timelog.objects.filter(task=task).last()
    #
    #     if log is not None and log.is_running is True:
    #         raise ValidationError('You cannot start task')
    #     else:
    #         log = Timelog.objects.create(
    #             task=task,
    #             start=validated_data['start'],
    #             stop=validated_data['start'] + timezone.timedelta(minutes=validated_data['duration']),
    #             duration=validated_data['duration'],
    #             is_running=False,
    #             owner=user
    #         )
    #
    #         log.save()
    #
    #         return Response({'status': HTTP_200_OK, 'time spent': log.duration})

class SearchTaskView(GenericAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get(self, request, value):
        tasks = Task.objects.filter(title__icontains=value)

        return Response(TaskSerializer(tasks, many=True).data)
