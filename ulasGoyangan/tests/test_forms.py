from django.test import TestCase

from ulasGoyangan.forms import ReviewForm


class ReviewFormTest(TestCase):
    def test_valid_form(self):
        form_data = {'rating': 4, 'comment': 'Nice place'}
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_empty_fields(self):
        form = ReviewForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)
        self.assertIn('comment', form.errors)

    def test_invalid_form_invalid_rating(self):
        form_data = {'rating': 'invalid', 'comment': 'Test comment'}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)
