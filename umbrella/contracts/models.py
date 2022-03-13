from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Lease(models.Model):
    id = models.BigAutoField(primary_key=True)
    file_name = models.CharField(max_length=512, blank=True, null=True)
    pdf = models.BinaryField(blank=True, null=True)
    txt = models.TextField(blank=True, null=True)
    extracted = models.JSONField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    createdon = models.DateTimeField(blank=True, null=True)
    createdby = models.CharField(max_length=128, blank=True, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True)
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
    created_by_django_user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    @property
    def status(self):
        return 'Not implemented'

    class Meta:
        # managed = False
        db_table = 'lease'
