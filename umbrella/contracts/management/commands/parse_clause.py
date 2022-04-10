from pathlib import Path

from django.core.management import CommandError
from django.core.management.base import BaseCommand

from umbrella.contracts.utils import parse_clause_json


class Command(BaseCommand):
    help = 'Parse clause json'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        file_path = Path(options['file_path'])
        if not file_path.is_file():
            raise CommandError("Invalid file path.")

        parse_clause_json(str(file_path))
