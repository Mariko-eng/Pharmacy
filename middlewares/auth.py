# authentication_backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class AuthenticationBackend(ModelBackend):
    def authenticate(self, request, company=None, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        if username is None or password is None:
            return None
        
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None
        
        # Check if the user is a superuser
        if user.is_superuser:
            if user.check_password(password):
                return user
        else:
            if company is None:
                return None

            try:
                user = UserModel.objects.get(school=company,username=username)
            except UserModel.DoesNotExist:
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
