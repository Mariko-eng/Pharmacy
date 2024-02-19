from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from utils.groups.default_roles import DefaultRoles
from utils.permissions.user import user_app_admin_permissions


def init_app_groups():
    default_app_level_roles = [
        DefaultRoles.APP_ADMIN,
    ]

    for item in default_app_level_roles:
        # role_name = item.replace(" ", "-") 
        role_name = item # No  need to replace space with _ since this group is global
        group_name = f"{role_name}"

        group, created = Group.objects.get_or_create(name=group_name)
        for codename, description in user_app_admin_permissions:
            user_app_permission, created = Permission.objects.get_or_create(codename=codename)
            group.permissions.add(user_app_permission)
