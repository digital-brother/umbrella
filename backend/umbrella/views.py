from django.shortcuts import render

from rest_framework import viewsets


from .serializers import  LeaseSerializer
from .models import Lease


class LeaseViewSet(viewsets.ModelViewSet):
    queryset = Lease.objects.all().order_by('file_name')
    serializer_class = LeaseSerializer
