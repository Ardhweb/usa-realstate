# backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class ObBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if '@' in username:
            try:
                user = User.objects.get(email=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None
        else:
            return super().authenticate(request, username=username, password=password, **kwargs)
