from latch.models import LatchSetup, UserProfile
from latch.latch_sdk_python import Latch


def instance():
    if not LatchSetup.objects.exists():
        return None
    setup = LatchSetup.objects.get(id=1)
    return Latch(setup.latch_appid, setup.latch_secret)


def appid():
    if not LatchSetup.objects.exists():
        return None
    setup = LatchSetup.objects.get(id=1)
    return setup.latch_appid


def accountid(user):
    try:
        acc_id = user.userprofile.latch_accountId
        return acc_id
    except Exception as e:
        return None


def get_or_create_profile(user):
    profile = None
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    return profile


def save_user_accountid(user, acc_id):
    profile = get_or_create_profile(user)
    profile.latch_accountId = acc_id
    profile.save()


def delete_user_account_id(acc_id):
    try:
        UserProfile.objects.get(latch_accountId=acc_id).delete()
        return True
    except UserProfile.DoesNotExist:
        return None
