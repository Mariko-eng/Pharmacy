from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from user.constants.roles import DefaultRoles
from user.constants.permissions.user import superuser_permissions
 

def init_app_groups():
    roles =  [ DefaultRoles.APP_ADMIN ] # Root Admin is also a superuser, so no need to add it

    all_permissions_set = set(Permission.objects.all()) # Use a set insteead of a list
    # Exclude superuser permissions
    excluded_permissions = [Permission.objects.get(codename=codename, name=description) for codename, description in superuser_permissions]

    excluded_permissions_set = set(excluded_permissions)

    for item in roles:
        # role_name = item.replace(" ", "-") 
        role_name = item # No  need to replace space with _ since this group is global
        group_name = f"{role_name}"

        group, created = Group.objects.get_or_create(name=group_name)

        for perm in all_permissions_set - excluded_permissions_set:
            group.permissions.add(perm)

