import logging
import os
import uuid

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from umbrella.contracts.models import Lease
from umbrella.contracts.serializers import GetAddFilePresignedUrlSerializer
from umbrella.contracts.serializers import UploadsSerializer


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


class GetAddFilePresignedUrlView(GenericAPIView):
    serializer_class = GetAddFilePresignedUrlSerializer

    def generate_modified_file_name(self, file_name):
        _, file_extension = os.path.splitext(file_name)
        file_uuid = uuid.uuid4()
        return f"{file_uuid}{file_extension}"

    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        file_name = serializer.validated_data['file_name']
        file_size = serializer.validated_data['file_size']

        response = create_presigned_post(settings.AWS_CONTRACT_BUCKET_NAME, file_name)
        if response is None:
            raise APIException({'aws_error': 'Unable to get a presigned url from AWS'})

        Lease.objects.create(
            file_name=file_name,
            modified_file_name=self.generate_modified_file_name(file_name),
            createdby=request.user,
            file_size=file_size,
            createdon=timezone.now(),
        )

        return Response(response)


class UploadsView(ListAPIView):
    queryset = Lease.objects.all()
    serializer_class = UploadsSerializer
