"""Thread create, retrieve and delete  tests"""
import json

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework import status


class MessageTestCase(TestCase):
    fixtures = ['users.json', 'threads.json', 'messages.json']

    def setUp(self):
        """Setting data for test."""

        self.username = 'TestUser'
        self.password = 'hYT!hA8F.!JK4Ds'
        self.user = User.objects.get(
            username=self.username)

        self.data = {
            'username': self.username,
            'password': self.password
        }
        self.client = APIClient()
        response = self.client.post('/auth-jwt/', self.data, format='json')
        self.token = response.data['token']
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_9_post_message(self):
        """Test Message create with correct data"""
        post_data = {
            "text": "testscasetest",
            "sender": 2,
            "thread": 4,
            }

        response = self.client.post('/api/create_message/', data=json.dumps(post_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(9, response.data.get('id'))

    def test_10_post_message(self):
        """Test Message create with incorrect thread"""
        post_data = {
            "text": "testscasetest",
            "sender": 2,
            "thread": 5,
            }

        with self.assertRaises(ValueError):
            self.client.post('/api/create_message/', data=json.dumps(post_data), content_type='application/json')

    def test_11_read_messages(self):
        """Test Message Update "is_read" with correct data"""
        post_data = {
            "message_ids": [1, 2]
            }

        response = self.client.put('/api/read_messages/', data=json.dumps(post_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_12_read_messages(self):
        """Test Message Update "is_read" with incorrect data"""
        post_data = {
            }
        expected_result = {'message_ids': ['This field is required.']}
        response = self.client.put('/api/read_messages/', data=json.dumps(post_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(expected_result, response.data)

    def test_13_unread_messages(self):
        """Test Message unread messages count with correct data"""

        response = self.client.get('/api/unread_messages/', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

