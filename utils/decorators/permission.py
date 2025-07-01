from functools import wraps
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from user.constants.roles import DefaultRoles
from company.models import Company, Store
from django.contrib import messages
from django.http import Http404

def custom_permission_required(perm, raise_exception=False):
    """
    Custom permission_required decorator that first checks if the user belongs
    to 'root' or 'admin' groups before performing the permission check.
    """

    def check_group_membership(user):
        # Check if user belongs to 'root' or 'admin' groups
        # root_admin_groups = ['root', 'admin']
        root_admin_groups = [role[0] for role in DefaultRoles.choices if role[0] in [DefaultRoles.ROOT_ADMIN, DefaultRoles.APP_ADMIN]]
        user_groups = user.groups.values_list('name', flat=True)
        for group in root_admin_groups:
            if group in user_groups:
                return True
        return False

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # First, check if user is in 'root' or 'admin' groups
            if check_group_membership(request.user):
                return view_func(request, *args, **kwargs)
            else:
                # If not in 'root' or 'admin' groups, proceed with permission check
                return permission_required(perm, raise_exception=raise_exception)(view_func)(request, *args, **kwargs)

        return wrapped_view

    return decorator


def user_has_permission(view_func):
    @wraps(view_func)
    def wrapper(request, store_id, *args, **kwargs):

        user = request.user
        app_admin_groups = [role[0] for role in DefaultRoles.choices if role[0] in [DefaultRoles.ROOT_ADMIN, DefaultRoles.APP_ADMIN]]
        user_groups = user.groups.values_list('name', flat=True)
        for group in app_admin_groups:
            if group in user_groups:
                return view_func(request, store_id, *args, **kwargs)

        # Get the store object
        store = get_object_or_404(Store, pk=store_id)
        
        # Check if the logged-in user is associated with the store
        # if request.user.is_authenticated and request.user.company == store.company:
        if request.user.is_authenticated and request.user.store == store:
            return view_func(request, store_id, *args, **kwargs)
        else:
            # Redirect to a login URL or show an error message
            messages.error(request, "You do not have permission to access this page.")
            raise Http404
            # return redirect(reverse('login'))  # Adjust this URL name based on your project
        
    return wrapper