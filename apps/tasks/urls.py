from django.urls import path

from apps.tasks.views import TaskCreateView, TaskListView, TaskItemView, MyTaskView, CompletedTaskView, AssignTaskView, \
    CompleteTaskView, DeleteTaskView

urlpatterns = [
    path('task-create/', TaskCreateView.as_view(), name='task-create'),
    path('task-list/', TaskListView.as_view(), name='task-list'),
    path('task/<int:pk>/', TaskItemView.as_view(), name='task-item'),
    path('my-task/', MyTaskView.as_view(), name='my-task'),
    path('competed-task/', CompletedTaskView.as_view(), name='competed-task'),
    path('assign-task/<int:task_id>/<int:user_id>/', AssignTaskView.as_view(), name='assign-task'),
    path('complete-task/<int:pk>/', CompleteTaskView.as_view(), name='complete-task'),
    path('delete-task/<int:pk>/', DeleteTaskView.as_view(), name='delete-task'),
]
