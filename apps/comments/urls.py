from django.urls import path

from apps.comments.views import CreateCommentView

urlpatterns = [
    path('create-comment/', CreateCommentView.as_view(), name='create-comment'),
]
