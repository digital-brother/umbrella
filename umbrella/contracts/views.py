import logging

import boto3
import requests
from botocore.exceptions import ClientError
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from umbrella.config.common import ROOT_DIR
from umbrella.contracts.models import Lease
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


class GetAddFilePresignedUrlSerializer(serializers.Serializer):
    file_name = serializers.CharField()
    file_size = serializers.IntegerField()


class GetAddFilePresignedUrlView(GenericAPIView):
    serializer_class = GetAddFilePresignedUrlSerializer

    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        # TODO: Get rid of self once testing is done (needed in AddFileView)
        self.file_name = serializer.validated_data['file_name']
        self.file_size = serializer.validated_data['file_size']

        self.response = create_presigned_post(settings.AWS_CONTRACT_BUCKET_NAME, self.file_name)

        Lease.objects.create(
            file_name=self.file_name,
            # TODO: generate once algorithm is provided by Riasat
            modified_file_name=None,  # Generated on BE
            # TODO: change fk to django user
            createdby='FRONTIER',
            file_size=self.file_size,
            createdon=timezone.now(),
            # TODO: remove onc createdby is working
            created_by_django_user=request.user
        )

        return Response(self.response)


class AddFileView(GetAddFilePresignedUrlView):
    def get(self, request):
        super().get(request)

        # Demonstrate how another Python program can use the presigned URL to upload a file
        file_path = ROOT_DIR / f'umbrella/contracts/{self.file_name}'
        with open(file_path, 'rb') as f:
            files = {'file': (self.file_name, f)}
            http_response = requests.post(self.response['url'], data=self.response['fields'], files=files)
        # If successful, returns HTTP status code 204
        msg = f'File upload HTTP status code: {http_response.status_code}'

        return Response(msg)


class UploadsView(ListAPIView):
    queryset = Lease.objects.all()
    serializer_class = UploadsSerializer
