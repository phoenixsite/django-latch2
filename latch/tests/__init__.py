from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User

from latch.models import LatchSetup, UserProfile

class LatchTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.latch_setup = LatchSetup.objects.create(
            latch_appid="abcdefghijklmnopqrst",
            latch_secret="abcdefghijklmnopqrstuvwxyzabcdefghijklmno",
        )

        self.paired_user = User.objects.create_user(
            username="paired", email="paired@mail.com", password="password"
        )

        self.paired_profile = UserProfile.objects.create(
            user=self.paired_user,
            latch_accountId="abcdefghijlkmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijkl",
        )

        self.unpaired_user = User.objects.create_user(
            username="unpaired", email="unpaired@mail.com", password="password"
        )