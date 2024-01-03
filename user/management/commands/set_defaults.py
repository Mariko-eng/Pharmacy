# myapp/management/commands/set_defaults.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from user.permissions import DefaultGroups, DefaultPermissions  # Adjust the import based on your project structure

class Command(BaseCommand):
    help = 'Sets default groups and permissions'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting default groups and permissions...'))

        # Create default groups
        for group_name, _ in DefaultGroups.choices:
            group, created = Group.objects.get_or_create(name=group_name)

            # Assign default permissions to each group
            if created:
                self.assign_default_permissions(group, group_name)

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
