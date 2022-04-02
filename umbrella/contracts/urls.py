from django.urls import path

from umbrella.contracts.views import GetAddFilePresignedUrlView, LeaseListView

urlpatterns = [
    path('get-add-file-presigned-url/', GetAddFilePresignedUrlView.as_view(), name='lease-create'),
    path('uploads/', LeaseListView.as_view(), name='lease-list'),
]
