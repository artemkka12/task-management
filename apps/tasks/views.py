from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer

from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet

from apps.tasks.models import Task, Timelog, Timer
from apps.tasks.serializers import (TaskSerializer, AssignTaskSerializer, ManualTimeLogSerializer, TimeLogSerializer,
                                    TopTasksSerializer, RetrieveTaskSerializer)
from config.settings import EMAIL_HOST_USER


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_fields = ('title', 'owner', 'completed')
    ordering = ('id', 'title',)
    search_fields = ('title',)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(owner=request.user)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = RetrieveTaskSerializer(instance=instance)
        return Response(serializer.data)

    @action(methods=['patch'], detail=True, serializer_class=Serializer)
    def complete_task(self, request, *args, **kwargs):
        task = self.get_object()
        task.completed = True
        task.save()

        users = User.objects.filter(comments__task_id=task.pk).distinct()
        for user in users:
            user.email_user('Hello!',
                            'Task which you commented was completed!'
                            , EMAIL_HOST_USER, )

        return Response({'status': HTTP_200_OK})

    @action(methods=['get'], detail=False, serializer_class=TaskSerializer)
    def view_my_tasks(self, request, *args, **kwargs):
        tasks = self.queryset.filter(owner=request.user)
        return Response(TaskSerializer(tasks, many=True).data)

    @action(methods=['get'], detail=False, serializer_class=TaskSerializer)
    def view_completed_tasks(self, request, *args, **kwargs):
        tasks = self.queryset.filter(completed=True)
        return Response(TaskSerializer(tasks, many=True).data)

    @action(methods=['patch'], detail=True, serializer_class=AssignTaskSerializer)
    def assign_task_to_user(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, instance=self.get_object())
        serializer.is_valid(raise_exception=True)
        task = serializer.save()

        task.owner.email_user('Hello!',
                              'A task was assigned to you!'
                              , EMAIL_HOST_USER, )

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

        return Response({'status': HTTP_200_OK, 'time_spent': timer.total_duration})

    @action(methods=['post'], detail=True, serializer_class=Serializer)
    def stop_time_log(self, request, *args, **kwargs):
        task = self.get_object()
        user = request.user
        timer = Timer.objects.filter(
            owner=user,
            task=task,
        ).last()
        timer.stop()

        return Response({'status': HTTP_200_OK, 'time_spent': timer.total_duration})

    @action(methods=['post'], detail=True, serializer_class=ManualTimeLogSerializer)
    def manual_time_log(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        stopped_at = serializer.validated_data['started_at'] + serializer.validated_data['duration'],
        log = serializer.save(task=self.get_object(), owner=request.user, stopped_at=stopped_at)

        return Response({'status': HTTP_200_OK, 'time_spent': log.duration})

    @action(methods=['get'], detail=True, serializer_class=TimeLogSerializer)
    def time_spent_by_task(self, request, *args, **kwargs):
        task = self.get_object()
        time_spent = Timelog.objects.filter(task=task).aggregate(sum=Sum('duration'))

        return Response({'time_spent': time_spent})

    @action(methods=['get'], detail=False)
    def amount_by_last_month(self, request, *args, **kwargs):
        last_month = timezone.now() - timezone.timedelta(days=timezone.now().day)
        amount_time = Timelog.objects.filter(started_at__gt=last_month).aggregate(sum=Sum('duration'))

        return Response({'amount_logged_time_by_last_month': amount_time})

    @method_decorator(cache_page(60))
    @action(methods=['get'], detail=False, serializer_class=TopTasksSerializer)
    def top_tasks_by_last_month(self, request, *args, **kwargs):
        last_month = timezone.now() - timezone.timedelta(days=timezone.now().day)
        tasks = Task.objects.filter(timelog__started_at__gt=last_month).annotate(sum=Sum('timelog__duration'))
        tasks = tasks.order_by('sum')[:20]

        return Response(TopTasksSerializer(tasks, many=True).data)
