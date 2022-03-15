from django.urls import path

from umbrella.contracts.views import GetAddFilePresignedUrlView, UploadsView

urlpatterns = [
    path('get-add-file-presigned-url/', GetAddFilePresignedUrlView.as_view(), name='get_add_file_presigned_url'),
    path('uploads/', UploadsView.as_view(), name='uploads'),
]
