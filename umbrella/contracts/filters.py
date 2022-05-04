import django_filters
from umbrella.contracts.models import Contract
from rest_framework import filters


class DocumentLibraryTagFilter(django_filters.FilterSet):
    tags = django_filters.BaseInFilter(field_name="tags__name", lookup_expr='in')

    class Meta:
        model = Contract
        fields = ('tags', )


class GroupFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see objects related to their group
    """

    def filter_queryset(self, request, queryset, view):
        user_groups = request.user.groups.all()
        return queryset.filter(groups__in=user_groups)