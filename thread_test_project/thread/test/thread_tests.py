"""Thread create, retrieve and delete  tests"""
import json

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status


class ThreadTestCase(TestCase):
    fixtures = ['users.json', 'threads.json', 'messages.json']

    def setUp(self):
        """Setting data for test."""

        self.username = 'TestCaseUser'
        self.password = 'test1234'
        self.user = User.objects.create_user(
            username=self.username, password=self.password)

        self.data = {
            'username': self.username,
            'password': self.password
        }
        client = APIClient()
        response = client.post('/auth-jwt/', self.data, format='json')
        self.token = response.data['token']
        self.client.credentials(
             HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_1_post_thread(self):
        """Test Thread create with correct data"""
        post_data = {
            "conversation_member": 1
            }

        resp = self.client.post('/api/create_thread/', data=json.dumps(post_data),
                                content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(6, resp.data.get('id'))
