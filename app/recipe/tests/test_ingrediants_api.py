from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingrediant

from recipe.serializers import TagSerializer, IngrediantSerializer

INGREDIANT_URL = reverse('recipe:ingrediant-list')

class PublicTestAPITests(TestCase):
	"""Test the publicly available tags API"""
	
	def setUp(self):
		self.client = APIClient()
		
	def test_login_required(self):
		"""Test that login is required for retriving ingrediant"""
		result = self.client.get(INGREDIANT_URL)
		self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTests(TestCase):
	"""Test the ingrediants can be retrived by authorized user."""
	
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			'test@test.com',
			'testpass'
		)
		self.client = APIClient()
		self.client.force_authenticate(self.user)
		
	def test_retrieve_ingrediants(self):
		"""Test retriving ingrediants"""
		Ingrediant.objects.create(user=self.user, name='Tomato')
		Ingrediant.objects.create(user=self.user, name='Salt')
		
		result = self.client.get(INGREDIANT_URL)
		ingrediants = Ingrediant.objects.all().order_by('-name')
		serializer = IngrediantSerializer(ingrediants, many=True)
		
		self.assertEqual(result.status_code, status.HTTP_200_OK)
		self.assertEqual(result.data, serializer.data)
	
	def test_ingrediants_limited_to_user(self):
		"""Test that only ingrediants returned are for the authenticated user"""
		user2 = get_user_model().objects.create_user(
			'test_2@test.com',
			'test2pass'
		)
		Ingrediant.objects.create(user=user2, name='Salt')
		ingrediant = Ingrediant.objects.create(user=self.user, name='Water')
		result = self.client.get(INGREDIANT_URL)
		
		self.assertEqual(result.status_code , status.HTTP_200_OK)
		self.assertEqual(len(result.data), 1)
		self.assertEqual(result.data[0]['name'], ingrediant.name)
		
		
	def test_create_ingrediant_successful(self):
		"""Testing creating a new ingrediant"""
		payload = {'name' : 'Test ingrediant'}
		self.client.post(INGREDIANT_URL, payload)
		exists = Ingrediant.objects.filter(
			user = self.user,
			name=payload['name']
		).exists()
		self.assertTrue(exists)
		
	def test_create_ingrediant_invlid(self):
		"""Test creating a new ingrediant with invalid payload"""
		payload={'name': ''}
		result = self.client.post(INGREDIANT_URL, payload)
		self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
		
		