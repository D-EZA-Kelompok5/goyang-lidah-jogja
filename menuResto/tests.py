from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from .models import Menu
from .forms import MenuForm
from main.models import UserProfile, Restaurant

class MenuRestoTest(TestCase):
    def setUp(self):
        # Create test users
        User = get_user_model()
        self.owner = User.objects.create_user(
            username='restaurantowner',
            password='testpass123'
        )
        self.regular_user = User.objects.create_user(
            username='regularuser',
            password='testpass123'
        )
        
        # Create profiles
        self.owner_profile, created = UserProfile.objects.get_or_create(user=self.owner)
        self.owner_profile.role = 'RESTAURANT_OWNER'
        self.owner_profile.save()
        
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.regular_user)
        self.user_profile.role = 'RESTAURANT_OWNER'
        self.user_profile.save()
        
        # Create test restaurant
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            description='A test restaurant',
            address='123 Test St',
            category='Test Category',
            price_range='$$',
            image='http://example.com/image.jpg',
            owner=self.owner_profile
        )
        
        # Create test menu
        self.menu = Menu.objects.create(
            restaurant=self.restaurant,
            name='Test Menu Item',
            description='A test menu item',
            price=10000,
            image='http://example.com/menu.jpg'
        )
        
        # Create client
        self.client = Client()

    def test_menu_model(self):
        """Test Menu model creation and string representation"""
        self.assertEqual(
            str(self.menu),
            f"Test Menu Item (Test Restaurant)"
        )
        self.assertEqual(self.menu.price, 10000)
        self.assertEqual(self.menu.description, 'A test menu item')

    def test_restaurant_dashboard_access(self):
        """Test restaurant dashboard access permissions"""
        dashboard_url = reverse('menuResto:restaurant_dashboard')
        
        # Test unauthorized access
        response = self.client.get(dashboard_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Test access with regular user
        self.client.login(username='regularuser', password='testpass123')
        response = self.client.get(dashboard_url)
        self.assertEqual(response.status_code, 200)  
        
        # Test access with restaurant owner
        self.client.login(username='restaurantowner', password='testpass123')
        response = self.client.get(dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant_dashboard.html')

    def test_restaurant_detail_menu(self):
        """Test restaurant detail menu view with different filters"""
        self.client.login(username='restaurantowner', password='testpass123')
        
        # Create additional menu items for testing filters
        Menu.objects.create(
            restaurant=self.restaurant,
            name='Cheap Item',
            price=5000
        )
        Menu.objects.create(
            restaurant=self.restaurant,
            name='Expensive Item',
            price=20000
        )
        
        # Test different menu filters
        filters = ['price_low', 'price_high', 'name_asc', 'name_desc']
        for filter_option in filters:
            response = self.client.get(
                reverse('menuResto:restaurant_detail_menu', 
                       kwargs={'restaurant_id': self.restaurant.id}),
                {'menu_filter': filter_option}
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn('menus', response.context)

    def test_create_menu(self):
        """Test menu creation"""
        self.client.login(username='restaurantowner', password='testpass123')
        
        # Test GET request
        response = self.client.get(
            reverse('menuResto:create_menu', 
                   kwargs={'restaurant_id': self.restaurant.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_menu.html')
        
        # Test POST request
        response = self.client.post(
            reverse('menuResto:create_menu', 
                   kwargs={'restaurant_id': self.restaurant.id}),
            {
                'name': 'New Menu Item',
                'description': 'New item description',
                'price': 15000,
                'image': 'http://example.com/newitem.jpg'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Menu.objects.filter(name='New Menu Item').exists()
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Menu item created successfully!')

    def test_edit_menu(self):
        """Test menu editing"""
        self.client.login(username='restaurantowner', password='testpass123')
        
        # Test GET request
        response = self.client.get(
            reverse('menuResto:edit_menu', kwargs={'pk': self.menu.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_menu.html')
        
        # Test POST request
        response = self.client.post(
            reverse('menuResto:edit_menu', kwargs={'pk': self.menu.pk}),
            {
                'name': 'Updated Menu Item',
                'description': 'Updated description',
                'price': 12000,
                'image': 'http://example.com/updated.jpg'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.menu.refresh_from_db()
        self.assertEqual(self.menu.name, 'Updated Menu Item')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Menu item updated successfully!')

    def test_delete_menu(self):
        """Test menu deletion"""
        self.client.login(username='restaurantowner', password='testpass123')
        
        response = self.client.post(
            reverse('menuResto:delete_menu', kwargs={'pk': self.menu.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Menu.objects.filter(pk=self.menu.pk).exists()
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Menu item deleted successfully!')

    def test_unauthorized_operations(self):
        """Test unauthorized menu operations"""
        # Login as regular user
        self.client.login(username='regularuser', password='testpass123')
        
        # Test create
        response = self.client.post(
            reverse('menuResto:create_menu', 
                   kwargs={'restaurant_id': self.restaurant.id}),
            {'name': 'Unauthorized Menu', 'price': 10000}
        )
        self.assertEqual(response.status_code, 403)  
        
        # Test delete
        response = self.client.post(
            reverse('menuResto:delete_menu', kwargs={'pk': self.menu.pk})
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Menu.objects.filter(pk=self.menu.pk).exists())