from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from umbrella.tasks.models import Task, Comment
from umbrella.tasks.serializers import TaskUpdateSerializer, TaskCommentSerializer, TaskSerializer


class TaskFilter(filters.FilterSet):
    assignees__id = filters.CharFilter(lookup_expr="icontains")

    ordering = filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('title', 'title'),
            ('contract_clause_type', 'clause'),
            ('due_date', 'due_date'),
            ('contract__file_name', 'contract'),
            ('progress', 'progress'),
            # ('status', 'status'), property fields doesn't work for filtering
        )
    )


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
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
