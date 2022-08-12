from django.test import TestCase

from .views import RegistrationView


# Create your tests here.
class TestViews(TestCase):
    """Test accounts views."""

    def test_index_reverse(self):
        v = RegistrationView()
        self.assertEqual(v.get_success_url(), "/")
