# authentication_backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class AuthenticationBackend(ModelBackend):
    def authenticate(self, request, company=None, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        if (username is None and kwargs.get(UserModel.EMAIL_FIELD) is None) or password is None:
            return None
                        
        # Try to get the user by email
        if username is None:
            username_or_email = kwargs.get(UserModel.EMAIL_FIELD)
            try:
                user = UserModel._default_manager.get(email=username_or_email)
            except UserModel.DoesNotExist:
                return None
        else:
            # Try to get the user by username
            try:
                user = UserModel._default_manager.get(username=username)
            except UserModel.DoesNotExist:
                return None
                    
        if user.is_superuser:
            if user.check_password(password):
                return user
        else:
            if company is None and user.userprofile.company is None:
                return None

            if user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
