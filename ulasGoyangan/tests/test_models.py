from django.test import TestCase
from django.contrib.auth import get_user_model
from menuResto.models import Menu, Restaurant  # Import Restaurant
from ulasGoyangan.models import Review
from django.utils import timezone

User = get_user_model()

class ReviewModelTest(TestCase):

    def setUp(self):
        # Create a restaurant first
        self.restaurant = Restaurant.objects.create(name="Test Restaurant", address="123 Street")

        # Then create a menu item associated with the restaurant
        self.menu = Menu.objects.create(name="Test Menu", description="Delicious food", price=50000, restaurant=self.restaurant)

        # Create a user for the review
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_create_review(self):
        # Test creating a review
        review = Review.objects.create(menu=self.menu, user=self.user, rating=4, comment="Great food!")
        self.assertEqual(review.menu, self.menu)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, "Great food!")
        self.assertIsNotNone(review.created_at)
        self.assertIsNone(review.last_edited)

    def test_edit_review_updates_last_edited(self):
        # Test updating the last_edited field when review is updated
        review = Review.objects.create(menu=self.menu, user=self.user, rating=4, comment="Good food!")
        review.comment = "Amazing food!"
        review.save()

        self.assertIsNotNone(review.last_edited)
        self.assertTrue(review.last_edited <= timezone.now())
    
    def test_str_method(self):
        # Test the __str__ method for correct output
        review = Review.objects.create(menu=self.menu, user=self.user, rating=5, comment="Excellent!")
        expected_str = f"Review by {self.user.username} for {self.menu.name}"
        self.assertEqual(str(review), expected_str)
