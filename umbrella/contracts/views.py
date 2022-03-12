import logging

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from umbrella.contracts.models import Lease


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


class GetAddFilePresignedUrlSerializer(serializers.Serializer):
    file_name = serializers.CharField()
    file_size = serializers.IntegerField()


class GetAddFilePresignedUrlView(GenericAPIView):
    serializer_class = GetAddFilePresignedUrlSerializer

    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        file_name = serializer.validated_data['file_name']
        file_size = serializer.validated_data['file_size']

        response = create_presigned_post(settings.AWS_CONTRACT_BUCKET_NAME, file_name)

        Lease.objects.create(
            file_name=file_name,
            # TODO: generate once algorithm is provided by Riasat
            modified_file_name=None,  # Generated on BE
            # TODO: change fk to django user
            createdby='FRONTIER',
            file_size=file_size,
            createdon=timezone.now(),
            # TODO: remove onc createdby is working
            created_by_django_user=request.user
        )

        return Response(response)
