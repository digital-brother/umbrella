from django.urls import path
from rest_framework.routers import DefaultRouter

from umbrella.tasks.views import TaskViewSet

urlpatterns = [

]

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns += router.urls
