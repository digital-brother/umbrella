from django.urls import path

from umbrella.contracts.views import ContractCreateView, ContractListView, ContractProcessedAWSWebhookView, \
    KDPClauseView, ClauseView, DocumentLibraryListView, contracts_statistics

urlpatterns = [
    path('get-add-file-presigned-url/', ContractCreateView.as_view(), name='contract-create'),
    path('uploads/', ContractListView.as_view(), name='contract-list'),
    path('<uuid:contract_id>/processed-aws-webhook/', ContractProcessedAWSWebhookView.as_view(),
         name='contract_processed_aws_webhook'),
    path('<uuid:contract_uuid>/kdp-clauses/<str:clause_type>/', KDPClauseView.as_view(), name='kdp_clause'),
    path('<uuid:contract_uuid>/clauses/<str:clause_type>/', ClauseView.as_view(), name='clause'),

    path('document-library/', DocumentLibraryListView.as_view(), name='document-library'),
    path('contracts-statistics/', contracts_statistics, name='contracts-statistics'),


]
