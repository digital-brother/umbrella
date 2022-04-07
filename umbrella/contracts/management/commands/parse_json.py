from django.core.management.base import BaseCommand

from umbrella.contracts.utils import parse_json


class Command(BaseCommand):
    help = 'Parse json'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        path = options['path']
        parse_json(path)
        print("Pars successfully")
