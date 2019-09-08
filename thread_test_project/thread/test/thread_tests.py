"""Thread create, retrieve and delete  tests"""
import json

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework import status


class ThreadTestCase(TestCase):
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

    def test_1_post_thread(self):
        """Test Thread create with correct data"""
        post_data = {
            "conversation_member": 1
            }

        response = self.client.post('/api/create_thread/', data=json.dumps(post_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, response.data.get('id'))

    def test_2_post_thread(self):
        """Test Thread when conversation member doesn't exist"""
        post_data = {
            "conversation_member": 10
            }
        with self.assertRaises(ValueError):
            self.client.post('/api/create_thread/', data=json.dumps(post_data), content_type='application/json')

    def test_3_post_thread(self):
        """Test Thread when conversation member not provided"""
        post_data = {
            }

        response = self.client.post('/api/create_thread/', data=json.dumps(post_data), content_type='application/json')

        expected_result = {'conversation_member': ['This field is required.']}
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(expected_result, response.data)

    def test_4_get_threads(self):
        """Test return all Threads for authenticated user """

        response = self.client.get('/api/threads/', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(response.data))

    def test_5_get_thread_messages(self):
        """ Test return all Threads for authenticated user,
            when the user is thread member
        """
        thread_id = 1

        response = self.client.get('/api/thread/?thread={}'.format(thread_id), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(5, response.data['count'])

    def test_6_get_thread_messages(self):
        """ Test return all Threads for authenticated user,
            when the user isn't thread member
        """
        thread_id = 5

        with self.assertRaises(ValueError):
            self.client.get('/api/thread/?thread={}'.format(thread_id), content_type='application/json')

    def test_7_delete_thread(self):
        """ Test delete Thread for authenticated user,
            when the user is thread member
        """
        thread_id = 1

        response = self.client.delete('/api/delete_thread/?thread={}'.format(thread_id), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_8_delete_thread(self):
        """ Test delete Thread for authenticated user,
            when the user isn't thread member
        """
        thread_id = 5

        with self.assertRaises(ValueError):
            self.client.delete('/api/delete_thread/?thread={}'.format(thread_id), content_type='application/json')

