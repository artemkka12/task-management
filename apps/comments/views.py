from drf_util.decorators import serialize_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.comments.models import Comment
from apps.comments.serializers import CommentSerializer


class CreateCommentView(GenericAPIView):
    serializer_class = CommentSerializer

    @serialize_decorator(CommentSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data
        comment = Comment.objects.create(
            text=validated_data['text'],
            task=validated_data['task']
        )

        comment.save()

        return Response({'comment id': comment.pk})


class CommentByTaskView(GenericAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get(self, request, pk):
        comments = Comment.objects.filter(task_id=pk)

        return Response(CommentSerializer(comments, many=True).data)



