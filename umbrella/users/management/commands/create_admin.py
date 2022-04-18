from uuid import UUID

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

from umbrella.contracts.tests.factories import ContractFactory
from umbrella.users.models import User

USERNAME = 'admin'
EMAIL = 'admin@gmail.com'
PASSWORD = 'admin'
GROUP = 'no_group'
TOKEN = '2e8c259163886711152ce41256fbedc1fa125569'
CONTRACT_UUID = UUID("6cb7fa02-457f-4e91-be84-3bfea7692d6b")


class Command(BaseCommand):
    help = 'Create an admin with a group if both are not exist'

    def handle(self, *args, **options):
        group_exists = Group.objects.filter(name=GROUP).exists()
        admin_exists = User.objects.filter(username=USERNAME).exists()
        error_msg = ''

        if group_exists:
            error_msg += f"Group '{GROUP}' already exists. "
        if admin_exists:
            error_msg += f"User '{USERNAME}' already exists. "
        if error_msg:
            print(error_msg)
            return

        admin_user = User.objects.create_superuser(username=USERNAME, email=EMAIL, password=PASSWORD)
        group = Group.objects.create(name=GROUP)
        admin_user.groups.set([group])
        Token.objects.filter(user=admin_user).update(key=TOKEN)
        print('Admin created successfully.')

        ContractFactory(
            id=CONTRACT_UUID,
            file_name='contract.pdf',
            created_by=admin_user,
        )
        print('Contract created successfully.')
