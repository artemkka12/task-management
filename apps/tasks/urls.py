from django.urls import path

from apps.tasks.views import TaskCreateView, TaskListView, TaskItemView

urlpatterns = [
    path('task-create/', TaskCreateView.as_view(), name='task-create'),
    path('task-list/', TaskListView.as_view(), name='task-list'),
    path('task/<int:pk>/', TaskItemView.as_view(), name='task-item'),
]
