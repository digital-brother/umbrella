from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from umbrella.contracts.models import Contract


class ContractStatisticPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page'

    def get_paginated_response(self, data):
        contracts_statistic = Contract.contracts_task_statistic()
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'contract_statistic': contracts_statistic,
            'results': data,
        })