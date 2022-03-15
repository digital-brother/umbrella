from rest_framework import serializers


class GetAddFilePresignedUrlSerializer(serializers.Serializer):
    file_name = serializers.CharField()
    file_size = serializers.IntegerField()
