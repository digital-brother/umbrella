from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError

from umbrella.users.models import User

USERNAME = 'admin'
EMAIL = 'admin@gmail.com'
PASSWORD = 'admin'
GROUP = 'no_group'


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
            raise CommandError(error_msg)

        admin_user = User.objects.create_superuser(username=USERNAME, email=EMAIL, password=PASSWORD)
        print(f"Created user '{USERNAME}' with email '{EMAIL}'.")

        group = Group.objects.create(name=GROUP)
        print(f"Created group '{GROUP}'.")

        admin_user.groups.set([group])
        print(f"Added user '{USERNAME}' to group '{GROUP}'.")
