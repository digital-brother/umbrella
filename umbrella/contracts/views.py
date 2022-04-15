import logging

import boto3
import uuid

from botocore.exceptions import ClientError
from django.conf import settings


from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.generics import ListAPIView

from rest_framework.response import Response


from umbrella.contracts.models import Contract, Node, CLAUSE_TYPE_KDP_TYPES_MAPPING
from umbrella.contracts.serializers import ContractSerializer, DocumentLibrarySerializer
from umbrella.contracts.serializers import GetAddFilePresignedUrlSerializer, KDPSerializer
from umbrella.contracts.tasks import load_aws_analytics_jsons_to_db



def create_presigned_post(bucket_name, object_name, fields=None, conditions=None, expiration=3600):
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


class ContractCreateView(CreateAPIView):
    serializer_class = GetAddFilePresignedUrlSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_name = serializer.validated_data['file_name']
        modified_file_name = Contract.generate_modified_file_name(file_name)

        response = create_presigned_post(settings.AWS_CONTRACT_BUCKET_NAME, modified_file_name)
        if response is None:
            raise APIException({'aws_error': 'Unable to get a presigned url from AWS'})

        self.perform_create(serializer)
        return Response({
            'presigned_url': response,
            'contract': serializer.data
        })

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


class ContractListView(ListAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    filter_backends = [GroupFilterBackend]


class AWSContractProcessedWebhookView(GenericAPIView):
    def post(self, request):
        field_name = 'contract_uuid'
        contract_uuid = request.data.get(field_name)

        contract = Contract.objects.filter(id=contract_uuid)
        if not contract:
            raise ValidationError({'contract': f"No contract with uuid {contract_uuid}"})

        load_aws_analytics_jsons_to_db.delay(contract_uuid)
        return Response(f"Downloaded contract {contract_uuid}")


class KDPClauseView(ListAPIView):
    """Iterate by KDPs, show Clause for each"""
    serializer_class = KDPSerializer

    def get_queryset(self):
        clause_type = self.kwargs['clause_type']
        kdp_types = CLAUSE_TYPE_KDP_TYPES_MAPPING[clause_type]

        contract_uuid = self.kwargs['contract_uuid']
        kdps = Node.objects.filter(clause__contract=contract_uuid, type__in=kdp_types)
        return kdps


class DocumentLibraryListView(ListAPIView):
    queryset = Contract.objects.filter(parent=None)
    serializer_class = DocumentLibrarySerializer


@api_view(('GET',))
def contracts_statistics(request, *args, **kwargs):
    data = {
        'contracts_statistic': Contract.contracts_task_statistic(),
    }
    return Response(data=data, status=status.HTTP_200_OK)











