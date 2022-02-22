from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet

from apps.tasks.models import Task
from apps.tasks.serializers import (TaskSerializer, AssignTaskSerializer)


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
                , 'artemkka2280@gmail.com',
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
                    , 'artemkka2280@gmail.com',
                    [user.email],
                )

        return Response(TaskSerializer(task).data)
    #
    # @action(methods=['post'], detail=True, serializer_class=Serializer)
    # def start(self, request, *args, **kwargs):
    #     task = self.get_object()
    #     user = request.user
    #     return Response('Done')


class SearchTaskView(GenericAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def get(self, request, value):
        tasks = Task.objects.filter(title__icontains=value)

        return Response(TaskSerializer(tasks, many=True).data)


# class StartLogTimeView(GenericAPIView):
#     serializer_class = TimeLogSerializer
#     queryset = Timelog.objects.all()
#
#     @serialize_decorator(TimeLogSerializer)
#     def post(self, request, pk):
#
#         log = Timelog.objects.create(
#             task=Task.objects.get(pk=pk),
#             start=timezone.now(),
#             stop=timezone.now()
#         )
#
#         log.save()
#
#         return Response({'log id': log.pk})
#
#
# class StopLogTimeView(GenericAPIView):
#     serializer_class = TimeLogSerializer
#     queryset = Timelog.objects.all()
#
#     @serialize_decorator(TimeLogSerializer)
#     def post(self, request, pk):
#
#         log = Timelog.objects.filter(task_id=pk).last()
#         log.stop = timezone.now()
#
#         log.save()
#
#         return Response({'spent time': log.stop - log.start})
