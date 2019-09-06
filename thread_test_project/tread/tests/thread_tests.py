"""Thread create, retrieve and delete  tests"""
import json

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status

class ThreadTestCase(TestCase):
    fixtures = ['users.json', 'threads.json', 'messages.json']
