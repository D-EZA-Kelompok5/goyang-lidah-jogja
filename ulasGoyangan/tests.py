from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import Review
from .forms import ReviewForm
from menuResto.models import Menu
from main.models import UserProfile, Restaurant
from django.contrib.messages import get_messages

class UlasGoyanganTest(TestCase):
    def setUp(self):
        # Create test user
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create second user for testing
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        
        # Create or get UserProfile
        self.profile, created = UserProfile.objects.get_or_create(user=self.user)
        self.profile.role = 'RESTAURANT_OWNER'
        self.profile.save()
        self.profile2 = UserProfile.objects.get_or_create(user=self.user2)
        
        # Create test restaurant
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            description='A test restaurant',
            address='123 Test St',
            category='Test Category',
            price_range='$$',
            image='http://example.com/image.jpg',
            owner=self.profile
        )
        
        # Create test menu
        self.menu = Menu.objects.create(
            name='Test Menu',
            price=10,
            restaurant=self.restaurant,
            description='Test menu description'
        )
        
        # Create test review
        self.review = Review.objects.create(
            menu=self.menu,
            user=self.user,
            rating=4,
            comment='Great food!'
        )
        
        # Create client and login
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')

    def test_review_model(self):
        """Test Review model creation and string representation"""
        self.assertEqual(str(self.review), f"Review by {self.user.username} for {self.menu.name}")
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.comment, 'Great food!')
        self.assertIsNotNone(self.review.created_at)
        self.assertIsNone(self.review.last_edited)

    def test_review_last_edited(self):
        """Test that last_edited is updated when review is edited"""
        original_time = self.review.created_at
        self.review.comment = 'Updated comment'
        self.review.save()
        self.assertIsNotNone(self.review.last_edited)
        self.assertGreater(self.review.last_edited, original_time)

    def test_submit_review_view(self):
        """Test submitting a new review"""
        response = self.client.post(
            reverse('ulasGoyangan:submit_review', kwargs={'menu_id': self.menu.id}),
            {
                'rating': 5,
                'comment': 'Excellent food!'
            }
        )
        self.assertEqual(response.status_code, 302)  # Should redirect after success
        self.assertTrue(Review.objects.filter(menu=self.menu, rating=5).exists())

    def test_edit_review_view(self):
        """Test editing an existing review"""
        response = self.client.post(
            reverse('ulasGoyangan:edit_review', kwargs={'review_id': self.review.id}),
            {
                'rating': 3,
                'comment': 'Updated review'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 3)
        self.assertEqual(self.review.comment, 'Updated review')

    def test_delete_review_view(self):
        """Test deleting a review"""
        response = self.client.post(
            reverse('ulasGoyangan:delete_review', kwargs={'review_id': self.review.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

    def test_unauthorized_edit_review(self):
        """Test that users cannot edit other users' reviews"""
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.post(
            reverse('ulasGoyangan:edit_review', kwargs={'review_id': self.review.id}),
            {
                'rating': 1,
                'comment': 'Trying to edit someone else\'s review'
            }
        )
        self.assertEqual(response.status_code, 404)
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 4)  # Rating should remain unchanged

    def test_unauthorized_delete_review(self):
        """Test that users cannot delete other users' reviews"""
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.post(
            reverse('ulasGoyangan:delete_review', kwargs={'review_id': self.review.id})
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Review.objects.filter(id=self.review.id).exists())

    def test_my_reviews_view(self):
        """Test viewing user's own reviews"""
        response = self.client.get(reverse('ulasGoyangan:my_reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_reviews.html')
        self.assertEqual(len(response.context['user_reviews']), 1)
        self.assertEqual(response.context['review_count'], 1)

    def test_menu_detail_view(self):
        """Test menu detail view with reviews"""
        response = self.client.get(
            reverse('ulasGoyangan:menu_detail', kwargs={'menu_id': self.menu.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu_detail.html')
        self.assertEqual(response.context['average_rating'], 4.0)
        self.assertIn('rating_distribution', response.context)

    def test_menu_comments_sorting(self):
        """Test different sorting options for menu comments"""
        # Create additional review for testing sort
        Review.objects.create(
            menu=self.menu,
            user=self.user2,
            rating=2,
            comment='Not great'
        )
        
        # Test latest sort
        response = self.client.get(
            reverse('ulasGoyangan:menu_comments', kwargs={'menu_id': self.menu.id}),
            {'sort': 'latest'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['reviews']), list(Review.objects.filter(menu=self.menu).order_by('-created_at')))
        
        # Test highest rating sort
        response = self.client.get(
            reverse('ulasGoyangan:menu_comments', kwargs={'menu_id': self.menu.id}),
            {'sort': 'highest'}
        )
        self.assertEqual(list(response.context['reviews']), list(Review.objects.filter(menu=self.menu).order_by('-rating')))

    def test_review_form_validation(self):
        """Test ReviewForm validation"""
        # Test invalid form
        form = ReviewForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)
        self.assertIn('comment', form.errors)
        
        # Test valid form
        form = ReviewForm(data={
            'rating': 5,
            'comment': 'Great food!'
        })
        self.assertTrue(form.is_valid())

    def test_review_count_update(self):
        """Test that user's review count is updated correctly"""
        initial_count = self.profile.review_count
        Review.objects.create(
            menu=self.menu,
            user=self.user,
            rating=5,
            comment='Another great meal!'
        )
        response = self.client.get(reverse('ulasGoyangan:my_reviews'))
        self.assertEqual(response.context['review_count'], initial_count + 2)

    def test_menu_rating_distribution(self):
        """Test calculation of rating distribution"""
        # Create reviews with different ratings
        Review.objects.create(menu=self.menu, user=self.user2, rating=5, comment='Excellent!')
        Review.objects.create(menu=self.menu, user=self.user2, rating=3, comment='Average')
        
        response = self.client.get(
            reverse('ulasGoyangan:menu_detail', kwargs={'menu_id': self.menu.id})
        )
        distribution = response.context['rating_distribution']
        self.assertTrue(all(key in distribution for key in ['1', '2', '3', '4', '5']))
        self.assertEqual(sum(distribution.values()), 99.99)

    def test_no_reviews_handling(self):
        """Test handling of menu with no reviews"""
        new_menu = Menu.objects.create(
            name='New Menu',
            price=15,
            restaurant=self.restaurant,
            description='New menu description'
        )
        response = self.client.get(
            reverse('ulasGoyangan:menu_detail', kwargs={'menu_id': new_menu.id})
        )
        self.assertEqual(response.context['average_rating'], 0)
        self.assertEqual(sum(response.context['rating_distribution'].values()), 0)