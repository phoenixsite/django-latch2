# pylint: disable=invalid-name,protected-access
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from latch.models import LatchSetup, UserProfile


class LatchAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Check if the user has Latch configured and, if so, check Latch status for the user.
        If user's account is disabled by Latch, raises
        :class:`django.core.exceptions.PermissionDenied`
        The methods delegate to the next authentication backend, by returning None when:
        * User's account has paired with Latch and account is unlocked.
        * User's account hasn't paired with Latch.
        """
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        user = UserModel._default_manager.get_by_natural_key(username)
        if not self.latch_permits_login(user):
            raise PermissionDenied

        return None

    @staticmethod
    def latch_permits_login(user):
        if not LatchSetup.objects.exists() or not UserProfile.accountid(user):
            # Always return on if is not configured or the user does not have latch configured
            return True
        l = LatchSetup.instance()
        # We need to extend the User Config to
        status_response = l.status(UserProfile.accountid(user))
        data = status_response.get_data()
        return data["operations"][LatchSetup.appid()]["status"] == "on"
