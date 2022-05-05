from uuid import UUID

from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

from umbrella.contracts.tests.factories import ContractFactory
from umbrella.users.models import User

USERNAME = 'admin'
EMAIL = 'admin@gmail.com'
PASSWORD = 'admin'
AUTH_TOKEN = '2e8c259163886711152ce41256fbedc1fa125569'
CONTRACT_UUID = UUID("6CB7FA02-457F-4E91-BE84-3BFEA7692D6B")


class Command(BaseCommand):
    help = 'Create an admin with a group if both are not exist'

    def handle(self, *args, **options):
        admin_exists = User.objects.filter(username=USERNAME).exists()
        error_msg = ''

        if admin_exists:
            error_msg += f"User '{USERNAME}' already exists. "
        if error_msg:
            print(error_msg)
            return

        admin_user = User.create_superuser_with_default_group(username=USERNAME, email=EMAIL, password=PASSWORD)
        Token.objects.filter(user=admin_user).update(key=AUTH_TOKEN)
        print('Admin created successfully.')

        ContractFactory(
            id=CONTRACT_UUID,
            file_name='contract.pdf',
            created_by=admin_user,
        )
        print('Contract created successfully.')
