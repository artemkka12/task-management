from django.contrib.auth.models import User
from django.core.mail import send_mail
from drf_util.decorators import serialize_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.comments.models import Comment
from apps.comments.serializers import CommentSerializer, CommentCreateSerializer
from apps.tasks.models import Task


class CreateCommentView(GenericAPIView):
    serializer_class = CommentCreateSerializer

    permission_classes = (IsAuthenticated, )

    @serialize_decorator(CommentCreateSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data
        comment = Comment.objects.create(
            text=validated_data['text'],
            task=validated_data['task'],
            owner=request.user
        )
        task = Task.objects.get(id=validated_data['task'].id)
        user = User.objects.get(id=task.owner.id)

        send_mail(
            'Hello!',
            'Your task was commented!'
            , 'artemkka2280@gmail.com',
            [user.email],
        )

        comment.save()

        return Response({'comment id': comment.pk})


class CommentByTaskView(GenericAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get(self, request, pk):
        comments = Comment.objects.filter(task_id=pk)

        return Response(CommentSerializer(comments, many=True).data)



