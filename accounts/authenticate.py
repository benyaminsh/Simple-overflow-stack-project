from django.contrib.auth.models import User


class EmailBackend:

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.filter(email=username).first()
            if user.check_password(password):
                return user
            else:
                return None

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):

        try:
            return User.objects.filter(pk=user_id).first()

        except User.DoesNotExist:
            return None
