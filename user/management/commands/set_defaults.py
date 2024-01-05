# myapp/management/commands/set_defaults.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from user.permissions import AccessGroups,RoleGroup, DefaultRoles, DefaultPermissions
from user.permissions import APP_ADMIN_GROUP_ROLES
from user.permissions import COMPANY_ADMIN_GROUP_ROLES
from user.permissions import STORE_ADMIN_GROUP_ROLES
from user.permissions import POS_ATTENDANT_GROUP_ROLES

class Command(BaseCommand):
    help = 'Sets default groups and permissions'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting default groups and permissions...'))

        # Create default groups
        for group_name, _ in DefaultRoles.choices:
            group, created = Group.objects.get_or_create(name=group_name)

            # Assign default permissions to each group
            if created:
                self.assign_default_permissions(group, group_name)
                self.create_default_role_groups()

        self.stdout.write(self.style.SUCCESS('Default groups and permissions set successfully.'))

    def assign_default_permissions(self, group, group_name):
        # Retrieve the default permissions for the group
        permissions = DefaultPermissions.perms.get(group_name, [])

        # Assign permissions to the group
        for permission_codename in permissions:
            try:
                permission = Permission.objects.get(codename=permission_codename)
                group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Warning: Permission {permission_codename} not found for group {group_name}"))

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

