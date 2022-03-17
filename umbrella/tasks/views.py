from rest_framework import viewsets, mixins
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from umbrella.tasks.models import Task, TaskChecklist
from umbrella.tasks.serializers import TaskSerializer, TaskChecklistSerializer, \
    TaskUpdateSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method in ['PUT', 'PATCH']:
            serializer_class = TaskUpdateSerializer

        return serializer_class


# class TaskChecklistViewSet(mixins.DestroyModelMixin,
#                            mixins.UpdateModelMixin,
#                            viewsets.GenericViewSet):
#     """
#     Update and Destroy task checklist item
#     """
#     queryset = TaskChecklist.objects.all()
#     serializer_class = TaskChecklistSerializer
#     permission_classes = [IsAuthenticated]
