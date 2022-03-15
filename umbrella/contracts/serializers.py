import os

from django.conf import settings
from rest_framework import serializers


class GetAddFilePresignedUrlSerializer(serializers.Serializer):
    file_name = serializers.CharField()
    file_size = serializers.IntegerField()

    def validate_file_name(self, value):
        _, file_extension = os.path.splitext(value)
        if file_extension not in settings.ALLOWED_FILE_UPLOAD_EXTENSIONS:
            allowed_file_extensions_str = ', '.join(settings.ALLOWED_FILE_UPLOAD_EXTENSIONS)
            err_msg = f"Invalid file extension. Allowed are: {allowed_file_extensions_str}"
            raise serializers.ValidationError(err_msg)
        return value
