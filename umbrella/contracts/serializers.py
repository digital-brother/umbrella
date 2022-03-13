from rest_framework import serializers

from umbrella.contracts.models import Lease


class UploadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lease
        fields = ['file_name', 'createdby', 'createdon', 'file_size', 'status']
