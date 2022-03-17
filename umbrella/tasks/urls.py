from django.urls import path
from rest_framework.routers import DefaultRouter

from umbrella.tasks.views import TaskViewSet

urlpatterns = [

]

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
# router.register(r'tasks-checklist', TaskChecklistViewSet)

urlpatterns += router.urls
