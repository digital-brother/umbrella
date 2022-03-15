from django.urls import path

from umbrella.contracts.views import GetAddFilePresignedUrlView

urlpatterns = [
    path('get-add-file-presigned-url/', GetAddFilePresignedUrlView.as_view(), name='get_add_file_presigned_url'),
]
