from django.urls import path

from umbrella.contracts.views import LeaseCreateView, LeaseListView

urlpatterns = [
    path('get-add-file-presigned-url/', LeaseCreateView.as_view(), name='lease-create'),
    path('uploads/', LeaseListView.as_view(), name='lease-list'),
]
