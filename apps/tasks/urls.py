from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.tasks.views import StartLogTimeView, StopLogTimeView, TaskViewSet

router = DefaultRouter()
router.register('tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('my-task/', MyTaskView.as_view(), name='my-task'),
    # path('competed-task/', CompletedTaskView.as_view(), name='competed-task'),
    # path('assign-task/<int:task_id>/<int:user_id>/', AssignTaskView.as_view(), name='assign-task'),
    # path('complete-task/<int:pk>/', CompleteTaskView.as_view(), name='complete-task'),
    # path('delete-task/<int:pk>/', DeleteTaskView.as_view(), name='delete-task'),
    # path('search-task/<str:value>', SearchTaskView.as_view(), name='search-task'),
    # path('start-log-time/<int:pk>/', StartLogTimeView.as_view(), name='start-log-time'),
    # path('stop-log-time/<int:pk>/', StopLogTimeView.as_view(), name='stop-log-time'),
]
