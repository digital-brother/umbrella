import os
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from rest_framework.exceptions import ValidationError

from umbrella.core.models import CustomModel

User = get_user_model()


class Contract(CustomModel):
    file_name = models.CharField(max_length=512)
    pdf = models.BinaryField(blank=True, null=True)
    txt = models.TextField(blank=True, null=True)
    extracted = models.JSONField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    modified_by = models.CharField(max_length=128, blank=True, null=True)
    active_flag = models.BooleanField(blank=True, null=True)
    contract_type = models.CharField(max_length=32, blank=True, null=True)
    textract = models.JSONField(blank=True, null=True)
    analytics_data = models.JSONField(blank=True, null=True)
    file_hash = models.TextField(unique=True)
    file_size = models.BigIntegerField()
    modified_file_name = models.CharField(max_length=256, unique=True)
    analytics_two = models.JSONField(blank=True, null=True)
    doc_type = models.CharField(max_length=258, blank=True, null=True)
    textract_done = models.BooleanField(blank=False, null=False, default=False)
    analytics_done = models.BooleanField(blank=False, null=False, default=False)
    normalization_done = models.BooleanField(blank=False, null=False, default=False)
    groups = models.ManyToManyField(Group, blank=True, related_name='contracts')

    def __str__(self):
        return self.file_name

    @classmethod
    def create(cls, file_name, **data):
        """
        Typical Django business logic placement
        (Two Scoops of Django 3.x, chapter 4.5.1 Service Layers)
        """
        data['modified_file_name'] = Contract.generate_modified_file_name(file_name)
        contract = super().create(file_name=file_name, **data)
        return contract

    def clean(self):
        errors = {}

        _, file_extension = os.path.splitext(self.file_name)
        if file_extension.lower() not in settings.ALLOWED_FILE_UPLOAD_EXTENSIONS:
            allowed_file_extensions_str = ', '.join(settings.ALLOWED_FILE_UPLOAD_EXTENSIONS)
            errors['file_name'] = f"Invalid file extension {file_extension}. Allowed are: {allowed_file_extensions_str}"

        if not self.created_by:
            errors['created_by'] = "created_by field is required"
            raise ValidationError(errors)

        realm = self.created_by.realm or User.NO_REALM
        is_duplicate = Contract.objects.filter(file_name=self.file_name, created_by__realm=realm).exists()
        if is_duplicate:
            errors['__all__'] = f"Duplicate file name {self.file_name} for realm {realm}"

        if errors:
            raise ValidationError(errors)

    @staticmethod
    def generate_modified_file_name(file_name):
        _, file_extension = os.path.splitext(file_name)
        file_uuid = uuid.uuid4()
        return f"{file_uuid}{file_extension}"

    @property
    def status(self):
        # TODO: Add status calculation
        return 'Not implemented'

    @classmethod
    def get_aws_downloads_dir(cls, contract_uuid):
        return f"{settings.AWS_DOWNLOADS_LOCAL_ROOT}/{contract_uuid.upper()}"


CLAUSE_TYPE_KDP_TYPES_MAPPING = {
    'term': ['start', 'end', 'duration', 'effective_date']
}


class Node(CustomModel):
    """Stores both Clause and KDP objects"""
    type = models.CharField(max_length=128)
    # Used for KDP node type, otherwise null
    clause = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    # Used for Clause node type, otherwise null
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, blank=True, null=True)

    content = models.JSONField(null=True, blank=True)
