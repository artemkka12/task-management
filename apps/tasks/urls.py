from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.tasks.views import TaskViewSet, SearchTaskView

router = DefaultRouter()
router.register('tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('search-task/<str:value>', SearchTaskView.as_view(), name='search-task'),
]
