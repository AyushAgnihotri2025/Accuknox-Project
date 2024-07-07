from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth.models import User

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        print("Here username", username, password)
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            print("Here2")
            pass
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def user_can_authenticate(self, user):
        return getattr(user, "is_active", True)
