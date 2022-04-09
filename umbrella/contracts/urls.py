from django.urls import path

from umbrella.contracts.views import LeaseCreateView, LeaseListView, AWSLeaseProcessedWebhookView, NodeView, \
    TermClauseView

urlpatterns = [
    path('get-add-file-presigned-url/', LeaseCreateView.as_view(), name='lease-create'),
    path('uploads/', LeaseListView.as_view(), name='lease-list'),
    path('aws-contract-processed-webhook/', AWSLeaseProcessedWebhookView.as_view(),
         name='aws-contract-processed-webhook'),
    path('node/', NodeView.as_view(), name='node'),
    path('<uuid:contract_uuid>/clauses/<str:clause_type>/', TermClauseView.as_view(), name='term_clause')
]
