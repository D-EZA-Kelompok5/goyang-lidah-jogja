from django.test import TestCase
from django.contrib.auth import get_user_model
from menuResto.models import Menu  # Import Restaurant
from ulasGoyangan.models import Review
from django.urls import reverse

User = get_user_model()

class ReviewViewsTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Create a restaurant and then a menu item linked to it

        self.menu = Menu.objects.create(name="Test Menu", price=10000, restaurant=self.restaurant)

        # Log in the user
        self.client.login(username="testuser", password="testpass")

        # Create a review
        self.review = Review.objects.create(menu=self.menu, user=self.user, rating=4, comment="Great food!")

    # Add test methods as needed...
