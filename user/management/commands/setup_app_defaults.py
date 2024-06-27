from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from user.constants.roles import DefaultRoles
from user.utils.init_app_groups import init_app_groups


class Command(BaseCommand):
    help = 'Sets default groups and permissions'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting default groups and permissions...'))

        # Create default groups
        for group_name, _ in DefaultRoles.choices:
            group, created = Group.objects.get_or_create(name=group_name)

        # Assign default permissions to each group
        self.create_app_groups()

        self.stdout.write(self.style.SUCCESS('Default groups and permissions set successfully.'))


    def create_app_groups(self, *args, **options):
        init_app_groups()