from latch import views
from latch.models import LatchSetup

from . import LatchTest

class UnconfiguredTest(LatchTest):
    def setUp(self):
        super().setUp()
        LatchSetup.objects.get(pk=1).delete()

    def test_pair_form_shows_unconfigured_latch_warning(self):
        request = self.factory.get("/pair")
        request.user = self.paired_user

        response = views.pair(request)

        self.assertContains(response, "Latch is not configured")

    def test_unpair_form_shows_unconfigured_latch_warning(self):
        request = self.factory.get("/unpair")
        request.user = self.paired_user

        response = views.pair(request)

        self.assertContains(response, "Latch is not configured")

    def test_status_shows_unconfigured_latch_warning(self):
        request = self.factory.get("/status")
        request.user = self.paired_user

        response = views.pair(request)

        self.assertContains(response, "Latch is not configured")
    