import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.exceptions import APIException

User = get_user_model()


# TODO: Rename to Contract
class Lease(models.Model):
    id = models.BigAutoField(primary_key=True)
    file_name = models.CharField(max_length=512, blank=True, null=True)
    pdf = models.BinaryField(blank=True, null=True)
    txt = models.TextField(blank=True, null=True)
    extracted = models.JSONField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    createdon = models.DateTimeField(auto_now_add=True)
    modifiedon = models.DateTimeField(auto_now=True)
    createdby = models.ForeignKey(User, on_delete=models.CASCADE)
    modifiedby = models.CharField(max_length=128, blank=True, null=True)
    activeflag = models.BooleanField(blank=True, null=True)
    contract_type = models.CharField(max_length=32, blank=True, null=True)
    textract = models.JSONField(blank=True, null=True)
    analyticsdata = models.JSONField(blank=True, null=True)
    pdf_hash = models.TextField(blank=True, null=True)
    file_size = models.BigIntegerField(blank=True, null=True)
    modified_file_name = models.CharField(max_length=256, blank=True, null=True)
    analytics2 = models.JSONField(blank=True, null=True)
    doc_type = models.CharField(max_length=258, blank=True, null=True)
    textract_done = models.BooleanField(blank=False, null=False, default=False)
    analytics_done = models.BooleanField(blank=False, null=False, default=False)
    normalization_done = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        db_table = 'lease'

    @classmethod
    def create(cls, file_name, createdby, **kwargs):
        errors = {}

        _, file_extension = os.path.splitext(file_name)
        if file_extension not in settings.ALLOWED_FILE_UPLOAD_EXTENSIONS:
            allowed_file_extensions_str = ', '.join(settings.ALLOWED_FILE_UPLOAD_EXTENSIONS)
            errors['file_name'] = f"Invalid file extension. Allowed are: {allowed_file_extensions_str}"

        realm = createdby.realm or User.NO_REALM
        is_duplicate = Lease.objects.filter(file_name=file_name, createdby__realm=realm).exists()
        if is_duplicate:
            errors['__all__'] = f"Duplicate file name for realm {realm}"

        if errors:
            raise APIException(errors)

        cls.objects.create(
            file_name=file_name,
            createdby=createdby,
            **kwargs
        )

    def __str__(self):
        return self.file_name
