from django.core.management.base import BaseCommand, CommandError
from rest_framework.exceptions import ValidationError
from rest_framework.fields import UUIDField

from umbrella.contracts.utils import download_s3_folder
from umbrella.core.exceptions import UmbrellaError


class Command(BaseCommand):
    help = 'Download contract by uuid'

    def add_arguments(self, parser):
        parser.add_argument('contract_uuid', type=str)

    def handle(self, *args, **options):
        contract_uuid = options['contract_uuid']
        cleaned_contract_uuid = self.validate_uuid(contract_uuid)
        s3_folder = str(cleaned_contract_uuid).upper()

        try:
            download_s3_folder(s3_folder)
        except UmbrellaError as err:
            raise CommandError(err.detail)

    def validate_uuid(self, value):
        try:
            cleaned_value = UUIDField().run_validation(value)
            return cleaned_value
        except ValidationError:
            raise CommandError(f"Invalid UUID '{value}'.")
