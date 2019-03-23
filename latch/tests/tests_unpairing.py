from django.contrib.auth.models import AnonymousUser

from latch import views

from . import LatchTest

class UnpairingTests(LatchTest):
    def test_pair_form_not_accesible_for_anonymous_user(self):
        request = self.factory.get("/pair")
        request.user = AnonymousUser()
        
        response = views.pair(request)

        self.assertEqual(response.status_code, 302)
