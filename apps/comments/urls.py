from django.urls import path

from apps.comments.views import CreateCommentView, CommentByTaskView

urlpatterns = [
    path('create-comment/', CreateCommentView.as_view(), name='create-comment'),
    path('task/<int:pk>/', CommentByTaskView.as_view(), name='comments-of-task')
]
