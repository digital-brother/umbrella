from django.urls import path

from umbrella.contracts.views import GetAddFilePresignedUrlView, LeaseListView

urlpatterns = [
    path('get-add-file-presigned-url/', GetAddFilePresignedUrlView.as_view(), name='get_add_file_presigned_url'),
    path('uploads/', LeaseListView.as_view(), name='lease-list'),
]
