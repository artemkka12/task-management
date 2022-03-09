from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.comments.serializers import CommentCreateSerializer
from config.settings import EMAIL_HOST_USER


class CreateCommentView(GenericAPIView):
    serializer_class = CommentCreateSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(owner=request.user)

        user = comment.task.owner

        user.email_user(
            'Hello!',
            'Your task was commented!'
            , EMAIL_HOST_USER, )

        return Response(serializer.data)
