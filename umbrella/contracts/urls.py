from django.urls import path

from umbrella.contracts.views import ContractCreateView, AWSContractProcessedWebhookView, \
    KDPClauseView, DocumentLibraryListView, ContractListView

urlpatterns = [
    path('get-add-file-presigned-url/', ContractCreateView.as_view(), name='contract-create'),
    path('uploads/', ContractListView.as_view(), name='contract-list'),
    path('aws-contract-processed-webhook/', AWSContractProcessedWebhookView.as_view(),
         name='aws-contract-processed-webhook'),
    path('<uuid:contract_uuid>/clauses/<str:clause_type>/', KDPClauseView.as_view(), name='kdp_clause'),

    path('get-contracts/', DocumentLibraryListView.as_view(), name='get_contracts'),


]
