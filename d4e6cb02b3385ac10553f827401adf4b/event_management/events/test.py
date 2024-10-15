from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token  
from rest_framework.test import APIClient  
from .models import Event  

class EventManagementAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()  
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.event_url = reverse('event-list-create')  

    def test_create_event(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) 
        
        
        response = self.client.post(self.event_url, {
            'title': 'Test Event',
            'description': 'This is a test event',
            'location': 'Test Location',
            'start_time': '2024-10-12T10:00:00Z',  
            'end_time': '2024-10-12T12:00:00Z',    #
            'is_public': True
        })
        print("Response Status Code:", response.status_code)
        print("Response Data:", response.data)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_events(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)  
        response = self.client.get(self.event_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
