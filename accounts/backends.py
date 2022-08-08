from django.db.models import Q
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        auth_type = settings.AUTH_AUTHENTICATION_TYPE
        if auth_type == 'username':
            return super().authenticate(request, username, password, **kwargs)
        user_model = get_user_model()
        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            if auth_type == 'both':
                user = user_model.objects.get(
                    Q(username__iexact=username) | Q(email__iexact=username)
                )
            else:
                user = user_model.objects.get(email__iexact=username)
        except user_model.DoesNotExist:
            return
        else:
            """
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            """
            if user.check_password(password):
                return user
            
