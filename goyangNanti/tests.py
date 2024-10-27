from django.test import TestCase
from .forms import WishlistForm

class WishlistFormTestCase(TestCase):
    def test_valid_form(self):
        form = WishlistForm(data={
            'catatan': 'Catatan yang valid',
            'status': 'SUDAH'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = WishlistForm(data={
            'catatan': 'Catatan yang valid',
            'status': 'INVALID_STATUS'  
        })
        self.assertFalse(form.is_valid())  
        self.assertIn('status', form.errors)  
