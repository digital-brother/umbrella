from django.urls import path

from umbrella.contracts.views import GetAddFilePresignedUrlView, AddFileView

urlpatterns = [
    path('get-add-file-presigned-url/', GetAddFilePresignedUrlView.as_view(), name='get_add_file_presigned_url'),
    path('add-file/', AddFileView.as_view(), name='add_file'),
]
