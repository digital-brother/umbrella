import os
import uuid
from hurry.filesize import size

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from rest_framework.exceptions import ValidationError

from umbrella.core.exceptions import UmbrellaError
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
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='children')
    modified_file_name = models.CharField(max_length=256, unique=True)
    analytics_two = models.JSONField(blank=True, null=True)
    doc_type = models.CharField(max_length=258, blank=True, null=True)
    textract_done = models.BooleanField(blank=False, null=False, default=False)
    analytics_done = models.BooleanField(blank=False, null=False, default=False)
    normalization_done = models.BooleanField(blank=False, null=False, default=False)
    groups = models.ManyToManyField(Group, blank=True, related_name='contracts')
    tags = models.ManyToManyField('Tag', related_name='contracts', blank=True)

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

        realm = self.created_by.realm or User.DEFAULT_REALM_NAME

        duplicate_contracts = Contract.objects.filter(file_name=self.file_name, created_by__realm=realm).exclude(
            pk=self.pk)
        if duplicate_contracts:
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

    @property
    def contracting_parties(self):
        return self.clauses.filter(type='contractingParties')

    @property
    def starts(self):
        return self.clauses.filter(type='start')

    @property
    def contract_types(self):
        return self.clauses.filter(type='contractType')

    @classmethod
    @property
    def contracts_count(cls):
        return cls.objects.all().count()

    @classmethod
    @property
    def contracts_with_task_count(cls):
        return Contract.objects.filter(tasks__isnull=False).count()

    @classmethod
    @property
    def contracts_without_task_count(cls):
        return Contract.objects.filter(tasks__contract=None).count()

    @classmethod
    @property
    def total_contracts_size(cls):
        total_byte_size = Contract.objects.all().aggregate(models.Sum('file_size'))
        return size(total_byte_size['file_size__sum'])

    @classmethod
    @property
    def statistic(cls):
        statistics = {
            'contracts_count': cls.contracts_count,
            'contracts_with_task_count': cls.contracts_with_task_count,
            'contracts_without_task_count': cls.contracts_without_task_count,
            'total_contracts_size': cls.total_contracts_size,
        }
        return statistics


class Tag(CustomModel):
    class Types(models.TextChoices):
        NATURE = 'nature', 'Nature'
        TYPE = 'type', 'Type'
        GROUP = 'group', 'Group'
        OTHERS = 'others', 'Others'

    name = models.CharField(max_length=128)
    type = models.CharField(max_length=128, choices=Types.choices)
    # Used for group Tags only
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, related_name='tags', blank=True, null=True)

    def __str__(self):
        return self.name


class Node(CustomModel):
    class Natures(models.TextChoices):
        CLAUSE = 'clause', 'Clause'
        KDP = 'KDP', 'KDP'

    """Stores both Clause and KDP objects"""
    type = models.CharField(max_length=128)
    # Used for KDP node type, otherwise null
    clause = models.ForeignKey("self", related_name='kdps', on_delete=models.CASCADE, blank=True, null=True)
    # Used for Clause node type, otherwise null
    contract = models.ForeignKey(Contract, related_name='clauses', on_delete=models.CASCADE, blank=True, null=True)

    content = models.JSONField(null=True, blank=True)

    @property
    def kind(self):
        if self.contract:
            return f"{self.type}_{self.Natures.CLAUSE}"
        elif self.clause:
            return f"{self.type}_{self.Natures.KDP}"
        else:
            raise UmbrellaError('Unknown node type')


class ClauseManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(contract__isnull=False)


class Clause(Node):
    objects = ClauseManager()

    class Meta:
        proxy = True

    def __str__(self):
        return f"{self.type} - {self.id}"


class KDPManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(clause__isnull=False)


class KDP(Node):
    objects = KDPManager()

    class Meta:
        proxy = True

    def __str__(self):
        return f"{self.type} - {self.id}"
