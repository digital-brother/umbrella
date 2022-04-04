import uuid

from django.core.management.base import BaseCommand, CommandError

from umbrella.contracts.utils import download_s3_folder
from umbrella.core.exceptions import UmbrellaException


class Command(BaseCommand):
    help = 'Download lease by uuid'

    def add_arguments(self, parser):
        parser.add_argument('lease_uuid', type=str)

    def handle(self, *args, **options):
        lease_uuid = options['lease_uuid']
        self.validate_uuid(lease_uuid)

        try:
            download_s3_folder(lease_uuid)
        except UmbrellaException as exc:
            msg = exc.args[0]
            raise CommandError(msg) from exc

    def validate_uuid(self, value):
        try:
            uuid.UUID(value)
        except ValueError:
            raise CommandError(f"Invalid UUID '{value}'.")
