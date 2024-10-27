from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from .models import Event, UserProfile
import json

class EventManagerDashboardTests(TestCase):
    def setUp(self):
        # Create test user and profile
        self.client = Client()
        self.user = User.objects.create_user(
            username='testmanager',
            password='testpass123'
        )
        
        self.profile, created = UserProfile.objects.get_or_create(user=self.user)
        self.profile.role = 'EVENT_MANAGER'
        self.profile.save()
        
        # Create non-manager user for testing permissions
        self.non_manager = User.objects.create_user(
            username='regular_user',
            password='testpass123'
        )
        
        self.non_manager_profile, created = UserProfile.objects.get_or_create(user=self.non_manager)
        self.non_manager_profile.role = 'EVENT_MANAGER'
        self.non_manager_profile.save()
        

        # Create sample event
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            date=timezone.now().date(),
            time=timezone.now().time(),
            location='Test Location',
            entrance_fee=Decimal('50.00'),
            image='http://example.com/image.jpg',
            created_by=self.profile
        )

        # Valid event data for testing
        self.valid_event_data = {
            'title': 'New Test Event',
            'description': 'New Description',
            'date': '2024-12-31',
            'time': '14:30',
            'location': 'New Location',
            'entrance_fee': '75.00',
            'image': 'http://example.com/new-image.jpg'
        }

    def test_dashboard_access_authenticated_manager(self):
        """Test that event managers can access the dashboard"""
        self.client.login(username='testmanager', password='testpass123')
        response = self.client.get(reverse('managerDashboard:event_manager_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_manager_dashboard.html')

    def test_dashboard_access_denied_unauthenticated(self):
        """Test that unauthenticated users cannot access the dashboard"""
        response = self.client.get(reverse('managerDashboard:event_manager_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_event_create_success(self):
        """Test successful event creation"""
        self.client.login(username='testmanager', password='testpass123')
        response = self.client.post(
            reverse('managerDashboard:event_create'),
            data=self.valid_event_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['status'], 'error')

    def test_event_update_success(self):
        """Test successful event update"""
        self.client.login(username='testmanager', password='testpass123')
        update_data = self.valid_event_data.copy()
        update_data['title'] = 'Updated Event Title'
        response = self.client.post(
            reverse('managerDashboard:event_update', kwargs={'pk': self.event.pk}),
            data=update_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['status'], 'error')
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, 'Test Event')

    def test_event_update_invalid_data(self):
        """Test event update with invalid data"""
        self.client.login(username='testmanager', password='testpass123')
        invalid_data = self.valid_event_data.copy()
        invalid_data['title'] = ''
        response = self.client.post(
            reverse('managerDashboard:event_update', kwargs={'pk': self.event.pk}),
            data=invalid_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['status'], 'error')
        self.assertIn('title', response_data['errors'])

    def test_event_delete_success(self):
        """Test successful event deletion"""
        self.client.login(username='testmanager', password='testpass123')
        response = self.client.post(
            reverse('managerDashboard:event_delete', kwargs={'pk': self.event.pk}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['status'], 'success')
        self.assertFalse(Event.objects.filter(pk=self.event.pk).exists())

    def test_event_delete_nonexistent(self):
        """Test deletion of non-existent event"""
        self.client.login(username='testmanager', password='testpass123')
        response = self.client.post(
            reverse('managerDashboard:event_delete', kwargs={'pk': 99999}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)