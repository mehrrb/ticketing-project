from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import Users
from .models import Ticket, Category, Notification

class TicketTests(APITestCase):
    def setUp(self):
        # Create test users
        self.user = Users.objects.create_user(
            email='test@example.com',
            password='testpass123',
            username='testuser'
        )
        self.admin_user = Users.objects.create_superuser(
            email='admin@example.com',
            password='admin123',
            username='admin'
        )
        self.other_user = Users.objects.create_user(
            email='other@example.com',
            password='other123',
            username='otheruser'
        )
        
        # Create test category
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Description'
        )
        
        # Create test ticket
        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Test Description',
            user=self.user,
            category=self.category,
            status='open',
            priority='medium'
        )
        
        self.client = APIClient()

    def test_ticket_list_authentication(self):
        """Test ticket list access with and without authentication"""
        # Test without login
        response = self.client.get('/tickets/ticket/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test with login
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/tickets/ticket/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_ticket(self):
        """Test creating new ticket"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Ticket',
            'description': 'New Description',
            'category': self.category.id,
            'priority': 'high'
        }
        response = self.client.post('/tickets/ticket/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 2)

    def test_ticket_creation_validation(self):
        """Test ticket creation validation"""
        self.client.force_authenticate(user=self.user)
        
        # Test with incomplete data
        data = {'title': 'Test'}  # without description
        response = self.client.post('/tickets/ticket/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_ticket_by_admin(self):
        """Test updating ticket by admin"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'status': 'in_progress',
            'reply': 'Admin reply'
        }
        response = self.client.patch(f'/tickets/ticket/{self.ticket.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, 'in_progress')
        self.assertEqual(self.ticket.reply, 'Admin reply')

    def test_notification_creation(self):
        """Test notification creation"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'status': 'closed'
        }
        response = self.client.patch(f'/tickets/ticket/{self.ticket.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Notification.objects.filter(
            user=self.ticket.user,
            ticket=self.ticket,
            notification_type='status_change'
        ).exists())

    def test_user_can_only_see_own_tickets(self):
        """Test user access restriction to own tickets"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get('/tickets/ticket/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_admin_can_see_all_tickets(self):
        """Test admin access to all tickets"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/tickets/ticket/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_ticket_filtering(self):
        """Test ticket filtering"""
        self.client.force_authenticate(user=self.admin_user)
        
        # Create additional ticket with different priority
        Ticket.objects.create(
            title='Urgent Ticket',
            description='Urgent Issue',
            user=self.user,
            status='open',
            priority='urgent'
        )
        
        # Test priority filter
        response = self.client.get('/tickets/ticket/?priority=urgent')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        # Test status filter
        response = self.client.get('/tickets/ticket/?status=open')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

class CategoryTests(APITestCase):
    def setUp(self):
        self.user = Users.objects.create_user(
            email='test@example.com',
            password='testpass123',
            username='testuser'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_category(self):
        """Test creating category"""
        data = {
            'name': 'New Category',
            'description': 'New Description'
        }
        response = self.client.post('/tickets/categories/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)

    def test_category_operations(self):
        """Test category operations"""
        # Test category creation
        data = {
            'name': 'New Category',
            'description': 'New Description'
        }
        response = self.client.post('/tickets/categories/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Test category listing
        response = self.client.get('/tickets/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
