import logging

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from rest_framework import filters
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from umbrella.contracts.models import Lease
from umbrella.contracts.serializers import GetAddFilePresignedUrlSerializer
from umbrella.contracts.serializers import LeaseSerializer


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


class GetAddFilePresignedUrlView(CreateAPIView):
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
