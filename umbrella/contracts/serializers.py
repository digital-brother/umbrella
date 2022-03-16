from rest_framework import serializers

from umbrella.contracts.models import Lease


class GetAddFilePresignedUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lease
        fields = ('file_name', 'file_size', 'file_hash')
