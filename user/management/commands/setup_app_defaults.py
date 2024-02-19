from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from utils.groups.access_groups import AccessGroups
from utils.groups.default_roles import DefaultRoles
from utils.groups.default_roles import APP_ADMIN_GROUP_ROLES
from utils.groups.default_roles import COMPANY_ADMIN_GROUP_ROLES
from utils.groups.default_roles import STORE_ADMIN_GROUP_ROLES
from utils.groups.default_roles import POS_ATTENDANT_GROUP_ROLES
from user.models import RoleGroup


class Command(BaseCommand):
    help = 'Sets default groups and permissions'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting default groups and permissions...'))

        # Create default groups
        for group_name, _ in DefaultRoles.choices:
            group, created = Group.objects.get_or_create(name=group_name)

        # Assign default permissions to each group
        self.create_default_role_groups()

        self.stdout.write(self.style.SUCCESS('Default groups and permissions set successfully.'))


    def create_default_role_groups(self):
        for access_group_name, _ in AccessGroups.choices:
            role_group, created = RoleGroup.objects.get_or_create(name = access_group_name)

            if created:
                if access_group_name == AccessGroups.APP_ADMIN:        
                    for item in APP_ADMIN_GROUP_ROLES:
                        group, created = Group.objects.get_or_create(name = item)
                        role_group.groups.add(group)

                if access_group_name == AccessGroups.COMPANY_ADMIN:        
                    for item in COMPANY_ADMIN_GROUP_ROLES:
                        group, created = Group.objects.get_or_create(name = item)
                        role_group.groups.add(group)

                if access_group_name == AccessGroups.STORE_ADMIN:        
                    for item in STORE_ADMIN_GROUP_ROLES:
                        group, created = Group.objects.get_or_create(name = item)
                        role_group.groups.add(group)

                if access_group_name == AccessGroups.POS_ATTENDANT:        
                    for item in POS_ATTENDANT_GROUP_ROLES:
                        group, created = Group.objects.get_or_create(name = item)
                        role_group.groups.add(group)

