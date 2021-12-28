from umbrella.models.Lease import Lease
from umbrella.serializers.lease_serializer import  LeaseSerializer
from rest_framework import viewsets

class LeaseViewSet(viewsets.ModelViewSet):
    queryset = Lease.objects.all().order_by('id');
    serializer_class = LeaseSerializer