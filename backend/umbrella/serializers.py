from rest_framework import serializers

from .models import Lease


class LeaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lease
        fields = ('id', 'file_name', 'pdf', 'txt', 'extracted', 'address', 'createdon', 'createdby','modifiedon', 'modifiedby', 'activeflag', 'contract_type', 'textract', 'analyticsdata', 'pdf_hash', 'file_size', 'modified_file_name', 'analytics2', 'doc_type')
    