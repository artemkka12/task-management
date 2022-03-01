from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.comments.models import Comment
from apps.comments.serializers import CommentSerializer, CommentCreateSerializer
from apps.tasks.models import Task
from config.settings import EMAIL_HOST_USER


class CreateCommentView(GenericAPIView):
    serializer_class = CommentCreateSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        serializer.save(owner=request.user)

        task = Task.objects.get(id=validated_data['task'].id)
        user = User.objects.get(id=task.owner.id)

        user.email_user(
            'Hello!',
            'Your task was commented!'
            , EMAIL_HOST_USER, )

        return Response(serializer.data)


class CommentByTaskView(GenericAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get(self, request, pk):
        comments = self.queryset.filter(task_id=pk)

        return Response(CommentSerializer(comments, many=True).data)


