from rest_framework import viewsets
from umbrella.models.Lease import Lease
from umbrella.serializers.lease_serializer import LeaseSerializer


class LeaseViewSet(viewsets.ModelViewSet):
    queryset = Lease.objects.all().order_by("id")
    serializer_class = LeaseSerializer
