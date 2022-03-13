from django.urls import path

from umbrella.contracts.views import GetAddFilePresignedUrlView, AddFileView, UploadsView

urlpatterns = [
    path('get-add-file-presigned-url/', GetAddFilePresignedUrlView.as_view(), name='get_add_file_presigned_url'),
    path('add-file/', AddFileView.as_view(), name='add_file'),
    path('uploads/', UploadsView.as_view(), name='uploads'),
]
