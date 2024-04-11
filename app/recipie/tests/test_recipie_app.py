"""
Tests for recipie APIs
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipie

from recipie.serializers import RecipieSerializer

RECIPIES_URL = reverse('recipie:recipie-list')

def create_recipie(user, **params):
    """
    Create and return a sample recipie.
    """
    defaults ={
        'title':'Sample Recipie',
        'time_minutes':22,
        'price':Decimal('5.25'),
        'description':'Sample description',
        'link':'http://example.com/recipie.pdf'

    }
    defaults.update(params)

    recipie = Recipie.objects.create(user=user, **defaults)
    return recipie


class PublicRecipieApiTests(TestCase):
    """Test unauthenticated API requests"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(RECIPIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipieApiTests(TestCase):
    """Test authenticated API requests"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipies(self):
        """Test retrieving a list of recipies"""
        create_recipie(user=self.user)
        create_recipie(user=self.user)

        res = self.client.get(RECIPIES_URL)

        recipies = Recipie.objects.all().order_by('-id')
        serializer = RecipieSerializer(recipies, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipie_limited_to_user(self):
        """
        Test list of recipies is limited to
        authenticated user.
        """
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'testpass123',
        )
        create_recipie(user=other_user)
        create_recipie(user=self.user)

        res = self.client.get(RECIPIES_URL)

        recipies = Recipie.objects.filter(user=self.user)
        serializer = RecipieSerializer(recipies,many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)
