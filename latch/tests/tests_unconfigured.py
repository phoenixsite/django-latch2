from django.test import override_settings

from . import LatchTest


class UnconfiguredTest(LatchTest):
    # We have to attach the decorator manually to each method because,
    # if used as a class decorator, ImproperlyConfigured exception will be raise
    # in LatchTest setUp method.
    @override_settings(LATCH_APP_ID=None)
    @override_settings(LATCH_APP_SECRET=None)
    def test_pair_form_shows_unconfigured_latch_warning(self):
        self.client.force_login(self.paired_user)
        response = self.client.get("/pair/", follow=True)

        self.assertContains(response, "Latch is not configured")

    @override_settings(LATCH_APP_ID=None)
    @override_settings(LATCH_APP_SECRET=None)
    def test_unpair_form_shows_unconfigured_latch_warning(self):
        self.client.force_login(self.paired_user)
        response = self.client.get("/unpair/", follow=True)

        self.assertContains(response, "Latch is not configured")

    @override_settings(LATCH_APP_ID=None)
    @override_settings(LATCH_APP_SECRET=None)
    def test_status_shows_unconfigured_latch_warning(self):
        self.client.force_login(self.paired_user)
        response = self.client.get("/status/")

        self.assertContains(response, "Latch is configured: <b>No</b>")
