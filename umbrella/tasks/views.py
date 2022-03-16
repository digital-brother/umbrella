from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from umbrella.tasks.models import Task
from umbrella.tasks.serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
