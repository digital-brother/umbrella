import django_filters
from django.db.models import QuerySet
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from umbrella.tasks.choices import StatusChoices
from umbrella.tasks.models import Task, Comment
from umbrella.tasks.serializers import TaskUpdateSerializer, TaskCommentSerializer, TaskSerializer


class CustomOrderingFilter(django_filters.OrderingFilter):
    def filter(self, qs, value):
        # OrderingFilter is CSV-based, so `value` is a list
        if any(v in ['status', '-status'] for v in value):
            new_qs = QuerySet()
            statuses = [x for x in StatusChoices.values]
            for status in statuses:
                ids_list = []
                for obj in qs:
                    if obj.status == status:
                        ids_list.append(obj.id)

            return super().filter(qs, value)

        return super().filter(qs, value)


class TaskFilter(filters.FilterSet):
    assignees__id = filters.CharFilter(lookup_expr="icontains")

    ordering = CustomOrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('title', 'title'),
            ('contract_clause_type', 'clause'),
            ('due_date', 'due_date'),
            ('contract__file_name', 'contract'),
            ('progress', 'progress'),
            # ('status', 'status'),
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
