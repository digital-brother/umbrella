from django.urls import path
from rest_framework.routers import DefaultRouter

from umbrella.tasks.views import TaskViewSet, TaskCommentCreateView

urlpatterns = [
    path('tasks/comments/', TaskCommentCreateView.as_view(), name="crate-task-comment"),
]

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns += router.urls
