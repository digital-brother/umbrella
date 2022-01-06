"""This file is responsible for converting lease objects
into data types understandable front-end frameworks."""

from rest_framework import serializers
from umbrella.models.lease import Lease
from umbrella.utils.lease_util import LeaseColumns


class LeaseSerializer(serializers.ModelSerializer):
    """Converting lease objects into data types understandable front-end frameworks."""

    class Meta:
        """A configuration class for lease serializer."""

        model = Lease
        fields = LeaseColumns
