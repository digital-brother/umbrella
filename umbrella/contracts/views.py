import logging
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from umbrella.contracts.models import Contract, Clause, KDP, Tag
from umbrella.contracts.serializers import ContractSerializer, DocumentLibrarySerializer, ClauseSerializer, \
    KDPClauseSerializer, TagSerializer, ContractClauseProcessedSerializer
from umbrella.contracts.tasks import parse_aws_clause_file_async
from umbrella.contracts.utils import _get_contract_from_clause_file_path
from umbrella.core.exceptions import UmbrellaError

User = get_user_model()


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


class ContractPresignedUrlView(CreateAPIView):
    """
    Creates a contract record in the database.
    Returns the contract data and a presigned url data for file upload from frontend.
    """
    serializer_class = ContractSerializer

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
        serializer.save(groups=user_groups, created_by=self.request.user)


class GroupFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see objects related to their group
    """

    def filter_queryset(self, request, queryset, view):
        user_groups = request.user.groups.all()
        return queryset.filter(groups__in=user_groups)


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    filter_backends = [GroupFilterBackend]

    def perform_create(self, serializer):
        user_groups = self.request.user.groups.all()
        serializer.save(groups=user_groups, created_by=self.request.user)


class ContractClauseProcessedView(GenericAPIView):
    serializer_class = ContractClauseProcessedSerializer
    permission_classes = []
    """
    Reads a clause json from AWS. Loads the clause and kdps to the database.
    """
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        aws_file_path_str = serializer.validated_data['aws_file_path']

        aws_file_path = Path(aws_file_path_str)
        try:
            contract = _get_contract_from_clause_file_path(aws_file_path)
        except UmbrellaError as err:
            raise ValidationError({'error': err.detail}) from err

        parse_aws_clause_file_async.delay(aws_file_path_str)

        response_data = {
            'message': f"Parsing {aws_file_path}",
            'contract': ContractSerializer(contract).data,
        }
        return Response(response_data)


class KDPClauseView(ListAPIView):
    """Iterate by KDPs, show Clause for each"""
    serializer_class = KDPClauseSerializer

    def get_queryset(self):
        clause_type = self.kwargs['clause_type']
        contract_uuid = self.kwargs['contract_uuid']
        kdps = KDP.objects.filter(clause__contract=contract_uuid, clause__type=clause_type)
        return kdps


class ClauseView(ListAPIView):
    """Iterate by Clauses"""
    serializer_class = ClauseSerializer

    def get_queryset(self):
        clause_type = self.kwargs['clause_type']
        contract_uuid = self.kwargs['contract_uuid']
        kdps = Clause.objects.filter(contract=contract_uuid, type=clause_type)
        return kdps


class DocumentLibraryListView(ListAPIView):
    queryset = Contract.objects.filter(parent=None)
    serializer_class = DocumentLibrarySerializer
    filter_backends = [GroupFilterBackend]


@api_view(('GET',))
def contracts_statistics(request, *args, **kwargs):
    data = {
        'contracts_statistic': Contract.statistics(),
    }
    return Response(data=data, status=status.HTTP_200_OK)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(Q(group=None) | Q(group__user=self.request.user))

    def perform_destroy(self, instance):
        tag_is_protected = instance.type != Tag.Types.OTHERS
        if tag_is_protected:
            raise ValidationError(f"'{instance.type}' tag cannot be deleted.")
        instance.delete()
