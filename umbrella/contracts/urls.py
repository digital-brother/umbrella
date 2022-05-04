from django.urls import path, include
from rest_framework import routers

from umbrella.contracts.views import ContractAWSPresignedUrlView, ContractClauseProcessedWebhookView, \
    KDPClauseView, ClauseView, DocumentLibraryListView, contracts_statistics, TagViewSet, \
    ContractViewSet

# TODO: check router usage
router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tag')
router.register(r'', ContractViewSet, basename="contract")

urlpatterns = [
    path('aws/presigned-url/', ContractAWSPresignedUrlView.as_view(), name='contract-aws-presigned-url'),
    path('aws/clause-processed-webhook/', ContractClauseProcessedWebhookView.as_view(),
         name='contract_clause_processed_webhook'),
    path('<uuid:contract_uuid>/kdp-clauses/<str:clause_type>/', KDPClauseView.as_view(), name='kdp_clause'),
    path('<uuid:contract_uuid>/clauses/<str:clause_type>/', ClauseView.as_view(), name='clause'),

    path('document-library/', DocumentLibraryListView.as_view(), name='document_library'),
    path('statistics/', contracts_statistics, name='contracts_statistics'),
    path('', include(router.urls)),
]
