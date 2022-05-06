from rest_framework_extensions.routers import ExtendedSimpleRouter

from umbrella.tasks.views import TaskViewSet, TaskCommentViewSet

urlpatterns = [
]

router = ExtendedSimpleRouter()
(
    router.register(r'tasks', TaskViewSet)
          .register(r'comments',
                    TaskCommentViewSet,
                    'tasks-comment',
                    parents_query_lookups=['task_id'])
)

urlpatterns += router.urls
