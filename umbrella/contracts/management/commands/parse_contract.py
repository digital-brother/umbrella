from django.core.management.base import BaseCommand

from umbrella.contracts.utils import parse_contract


class Command(BaseCommand):
    help = 'Parse clause json'

    def add_arguments(self, parser):
        parser.add_argument('contract_uuid', type=str)

    def handle(self, *args, **options):
        contract_uuid = options['contract_uuid']
        parse_contract(str(contract_uuid))
