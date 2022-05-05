import django_filters
from django_filters import rest_framework as filters


class DocumentLibraryFilter(filters.FilterSet):
    tags = django_filters.BaseInFilter(field_name="tags__name", lookup_expr='in')
    ordering = filters.OrderingFilter(
        fields=[
            ('file_name', 'file_name'),
            ('clauses__content__start_date', 'start_date'),
        ])


class GroupFilterBackend(filters.DjangoFilterBackend):
    """
    Filter that only allows users to see objects related to their group
    """

    def filter_queryset(self, request, queryset, view):
        user_groups = request.user.groups.all()
        return queryset.filter(groups__in=user_groups)


class TaskFilter(filters.FilterSet):
    assignees = filters.CharFilter(field_name='assignees_id', lookup_expr="icontains")

    ordering = filters.OrderingFilter(
        fields=['title', 'contract_clause_type', 'due_date', 'contract__file_name', 'progress', 'status']
    )
