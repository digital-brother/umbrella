from django.core.management.base import BaseCommand

from umbrella.contracts.utils import parse_aws_contract


class Command(BaseCommand):
    help = 'Parse contract from AWS folder'

    def add_arguments(self, parser):
        parser.add_argument('contract_id', type=str)

    def handle(self, *args, **options):
        contract_id = options['contract_id']
        parse_aws_contract(contract_id)
