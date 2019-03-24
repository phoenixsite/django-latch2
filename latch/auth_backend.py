# pytlint: disable=invalid-name
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from latch.models import LatchSetup, UserProfile


class LatchAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
            if not self.latch_permits_login(user):
                UserModel().set_password(password)
                return None
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
        except Exception as err:
            raise ValidationError("There was an unknown error: %s" % err)

    def latch_permits_login(self, user):
        if not LatchSetup.objects.exists() or not UserProfile.accountid(user):
            # Always return on if is not configured or the user does not have latch configured
            return True
        l = LatchSetup.instance()
        # We need to extend the User Config to
        data = l.status(UserProfile.accountid(user))
        d = data.get_data()
        return d["operations"][LatchSetup.appid()]["status"] == "on"
