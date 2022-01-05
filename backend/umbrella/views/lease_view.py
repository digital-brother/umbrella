"""This file is used for the 'lease' model CRUD API."""
from rest_framework import viewsets
from umbrella.models.lease import Lease
from umbrella.serializers import LeaseSerializer


class LeaseViewSet(viewsets.ModelViewSet):
    """A ViewSet for viewing and editing the Lease model."""
    queryset = Lease.objects.all().order_by("id")
    serializer_class = LeaseSerializer
