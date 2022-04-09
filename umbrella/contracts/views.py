import logging

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from rest_framework import filters
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.fields import UUIDField
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from umbrella.contracts.models import Lease, Node
from umbrella.contracts.serializers import GetAddFilePresignedUrlSerializer, KDPSerializer
from umbrella.contracts.serializers import LeaseSerializer
from umbrella.contracts.utils import download_s3_folder


def create_presigned_post(bucket_name, object_name,
        fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """

    # Generate a presigned S3 POST URL
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     Fields=fields,
                                                     Conditions=conditions,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL and required fields
    return response


class LeaseCreateView(CreateAPIView):
    serializer_class = GetAddFilePresignedUrlSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_name = serializer.validated_data['file_name']
        modified_file_name = Lease.generate_modified_file_name(file_name)
        response = create_presigned_post(settings.AWS_CONTRACT_BUCKET_NAME, modified_file_name)
        if response is None:
            raise APIException({'aws_error': 'Unable to get a presigned url from AWS'})

        self.perform_create(serializer)
        return Response(response)

    def perform_create(self, serializer):
        user_groups = self.request.user.groups.all()
        serializer.save(groups=user_groups)


class GroupFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see objects related to their group
    """

    def filter_queryset(self, request, queryset, view):
        user_groups = request.user.groups.all()
        return queryset.filter(groups__in=user_groups)


class LeaseListView(ListAPIView):
    queryset = Lease.objects.all()
    serializer_class = LeaseSerializer
    filter_backends = [GroupFilterBackend]


class AWSLeaseProcessedWebhookView(GenericAPIView):
    def post(self, request):
        field_name = 'contract_uuid'
        lease_uuid = request.data.get(field_name)

        try:
            cleaned_lease_uuid = UUIDField().run_validation(lease_uuid)
        except ValidationError as err:
            raise ValidationError({field_name: err.detail})

        s3_folder = str(cleaned_lease_uuid).upper()
        downloaded_files = download_s3_folder(s3_folder)
        return Response(downloaded_files)


class NodeView(ListAPIView):
    queryset = Node.objects.filter(clause__isnull=False)
    serializer_class = KDPSerializer


class TermClauseView(ListAPIView):
    serializer_class = KDPSerializer

    def get_queryset(self):
        clause_type_kdp_types_mapping = {
            'term': ['start', 'end', 'duration', 'effective_date']
        }
        clause_type = self.kwargs['clause_type']
        kdp_types = clause_type_kdp_types_mapping[clause_type]

        contract_uuid = self.kwargs['contract_uuid']
        kdps = Node.objects.filter(clause__lease=contract_uuid, type__in=kdp_types)
        return kdps
