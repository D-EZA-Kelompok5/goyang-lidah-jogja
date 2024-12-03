from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from .models import Tag, MenuTag
from menuResto.models import Menu
from main.models import UserProfile, Restaurant
from .forms import UserPreferencesForm

class UserPreferencesTest(TestCase):
    def setUp(self):
        # Create test user
        User = get_user_model()
        self.user = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        
        # Create regular user for testing customer views
        self.customer = User.objects.create_user(
            username='customer',
            password='customer123'
        )
        self.customer_profile, _ = UserProfile.objects.get_or_create(user=self.customer)
        self.customer_profile.role = 'CUSTOMER'
        self.customer_profile.save()
        
        # Create or get UserProfile and set role to 'RESTAURANT_OWNER'
        self.profile, created = UserProfile.objects.get_or_create(user=self.user)
        self.profile.role = 'RESTAURANT_OWNER'
        self.profile.save()
        
        # Create test tags
        self.tag = Tag.objects.create(name='Vegetarian')
        self.tag2 = Tag.objects.create(name='Spicy')
        self.tag3 = Tag.objects.create(name='Halal')
        
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            description='A test restaurant',
            address='123 Test St',
            category='Test Category',
            price_range='$$',
            image='http://example.com/image.jpg',
            owner=self.profile
        )
        self.menu = Menu.objects.create(
            name='Test Menu', 
            price=10, 
            restaurant_id=self.restaurant.id,
            description='Test menu description'
        )
        
        # Create client and login
        self.client = Client()
        self.client.login(username='testuser2', password='testpass123')

    def test_preferences_url_exists(self):
        """Test that preferences page exists and requires login"""
        # Test without login
        self.client.logout()
        response = self.client.get(reverse('userPreferences:edit_preferences'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        
        # Test with customer login
        self.client.login(username='customer', password='customer123')
        response = self.client.get(reverse('userPreferences:edit_preferences'))
        self.assertEqual(response.status_code, 200)  # Should be accessible to customers

    def test_preferences_using_correct_template(self):
        """Test that preferences page uses correct template"""
        self.client.login(username='customer', password='customer123')
        response = self.client.get(reverse('userPreferences:edit_preferences'))
        self.assertTemplateUsed(response, 'edit_preferences.html')

    def test_nonexistent_preferences_page(self):
        """Test accessing non-existent preferences page"""
        response = self.client.get('/preferences/nonexistent/')
        self.assertEqual(response.status_code, 404)

    def test_tag_creation(self):
        """Test tag creation and properties"""
        tag = Tag.objects.create(name='Gluten-Free')
        self.assertEqual(str(tag), 'Gluten-Free')
        self.assertEqual(tag.name, 'Gluten-Free')

    def test_unique_tag_constraint(self):
        """Test that tags must be unique"""
        with self.assertRaises(Exception):
            Tag.objects.create(name='Vegetarian')

    def test_menu_tag_relationship(self):
        """Test the relationship between tags and menus"""
        menu_tag = MenuTag.objects.create(
            tag=self.tag,
            menu=self.menu
        )
        self.assertEqual(self.tag.menus.count(), 1)
        self.assertEqual(self.menu.tags.first(), self.tag)
        # Test cascade deletion
        self.menu.delete()
        self.assertEqual(MenuTag.objects.filter(tag=self.tag).count(), 0)

    def test_preferences_update(self):
        """Test updating user preferences"""
        self.client.login(username='customer', password='customer123')
        response = self.client.post(
            reverse('userPreferences:edit_preferences'),
            {'preferences': [str(self.tag.id), str(self.tag2.id)]}
        )
        self.assertEqual(response.status_code, 302)  # Should redirect after success
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Your preferences have been updated successfully!')
        self.customer_profile.refresh_from_db()
        self.assertEqual(self.customer_profile.preferences.count(), 2)

    def test_empty_preferences(self):
        """Test submitting empty preferences"""
        self.client.login(username='customer', password='customer123')
        response = self.client.post(
            reverse('userPreferences:edit_preferences'),
            {'preferences': []}
        )
        self.assertEqual(response.status_code, 302)
        self.customer_profile.refresh_from_db()
        self.assertEqual(self.customer_profile.preferences.count(), 0)

    def test_preferences_display(self):
        """Test that all tags are displayed on preferences page"""
        self.client.login(username='customer', password='customer123')
        response = self.client.get(reverse('userPreferences:edit_preferences'))
        self.assertIn('all_tags', response.context)
        self.assertIn(self.tag, response.context['all_tags'])
        self.assertIn(self.tag2, response.context['all_tags'])
        self.assertIn(self.tag3, response.context['all_tags'])

    def test_user_current_preferences(self):
        """Test that user's current preferences are correctly shown"""
        self.client.login(username='customer', password='customer123')
        self.customer_profile.preferences.add(self.tag, self.tag2)
        response = self.client.get(reverse('userPreferences:edit_preferences'))
        self.assertIn('user_preferences', response.context)
        self.assertIn(self.tag, response.context['user_preferences'])
        self.assertIn(self.tag2, response.context['user_preferences'])

    def test_tag_str_method(self):
        """Test the string representation of Tag model"""
        self.assertEqual(str(self.tag), 'Vegetarian')

    def test_menutag_unique_together_constraint(self):
        """Test that MenuTag enforces unique_together constraint"""
        MenuTag.objects.create(tag=self.tag, menu=self.menu)
        with self.assertRaises(Exception):
            MenuTag.objects.create(tag=self.tag, menu=self.menu)

    def test_preferences_form_validation(self):
        """Test UserPreferencesForm validation"""
        form = UserPreferencesForm(instance=self.customer_profile)
        self.assertIn('preferences', form.fields)
        self.assertFalse(form.fields['preferences'].required)

    def test_tag_deletion_cascade(self):
        """Test that deleting a tag removes related MenuTag entries"""
        menu_tag = MenuTag.objects.create(tag=self.tag, menu=self.menu)
        self.tag.delete()
        self.assertEqual(MenuTag.objects.filter(menu=self.menu).count(), 0)

    def test_multiple_preferences_update(self):
        """Test updating preferences multiple times"""
        self.client.login(username='customer', password='customer123')
        
        # First update
        self.client.post(
            reverse('userPreferences:edit_preferences'),
            {'preferences': [str(self.tag.id)]}
        )
        self.customer_profile.refresh_from_db()
        self.assertEqual(self.customer_profile.preferences.count(), 1)
        
        # Second update
        self.client.post(
            reverse('userPreferences:edit_preferences'),
            {'preferences': [str(self.tag2.id), str(self.tag3.id)]}
        )
        self.customer_profile.refresh_from_db()
        self.assertEqual(self.customer_profile.preferences.count(), 2)