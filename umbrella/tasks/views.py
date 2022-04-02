from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from umbrella.tasks.models import Task, Comment
from umbrella.tasks.serializers import TaskUpdateSerializer, TaskCommentSerializer, TaskSerializer


class TaskFilter(filters.FilterSet):
    assignees__id = filters.CharFilter(lookup_expr="icontains")

    ordering = filters.OrderingFilter(
        fields=['title', 'contract_clause_type', 'due_date', 'contract__file_name', 'progress', 'status']
    )


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = TaskFilter

    def get_serializer_class(self):
        serializer_class = TaskSerializer

        if self.request.method in ['PUT', 'PATCH']:
            serializer_class = TaskUpdateSerializer

        return serializer_class


class TaskCommentCreateView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = TaskCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
