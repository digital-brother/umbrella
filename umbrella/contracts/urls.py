from django.urls import path

from umbrella.contracts.views import GetAddFilePresignedUrlView

urlpatterns = [
    path('get-add-file-presigned-url/', GetAddFilePresignedUrlView.as_view(), name='add_file'),
]
