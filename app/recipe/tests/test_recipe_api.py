from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingrediant

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id):
	"""Return recipe URL"""
	return reverse('recipe:recipe-detail', args=[recipe_id])

def sample_tag(user, name='Main course'):
	"""Creat and return a sample tag"""
	return Tag.objects.create(user=user, name=name)
	
def sample_ingrediant(user, name='Cinamon'):
	"""Create and return sampel integrediant"""
	return Ingrediant.objects.create(user=user, name=name)

def sample_recipe(user, **params):
	"""Create and return a sample recipe"""
	defaults = {
		'title': 'Sample recipe',
		'time_minutes': 10,
		'price': 5.00
	}
	defaults.update(params)
	return Recipe.objects.create(user=user, **defaults)
	
class PublicRecipeAPITests(TestCase):
	"""Test the un authenticated recipe access"""
	
	def setUp(self):
		self.client = APIClient()
		
	def test_auth_required(self):
		"""Test that authentication is required"""
		
		result = self.client.get(RECIPES_URL)
		self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeApiTests(TestCase):
	"""Test the authorized user recipe API"""
	
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			'test@test.com',
			'testpass'
		)
		self.client = APIClient()
		self.client.force_authenticate(self.user)
		
	def test_retrieve_recipe(self):
		"""Test recipe tags"""
		sample_recipe(user=self.user)
		
		result = self.client.get(RECIPES_URL)
		recipes = Recipe.objects.all().order_by('-id')
		serializer = RecipeSerializer(recipes, many=True)
		
		self.assertEqual(result.status_code, status.HTTP_200_OK)
		self.assertEqual(result.data, serializer.data)
	
	def test_recipes_limited_to_user(self):
		"""Test that recipes returned are for the authenticated user"""
		user2 = get_user_model().objects.create_user(
			'test_2@test.com',
			'test2pass'
		)
		sample_recipe(user=user2)
		sample_recipe(user=self.user)
		
		result = self.client.get(RECIPES_URL)
		
		recipes = Recipe.objects.filter(user=self.user)
		serializer = RecipeSerializer(recipes, many=True)
		
		self.assertEqual(result.status_code , status.HTTP_200_OK)
		self.assertEqual(len(result.data), 1)
		self.assertEqual(result.data, serializer.data)
	
	def test_view_recipe_detail(self):
		"""Test viewing recipe detail"""
		recipe = sample_recipe(user=self.user)
		recipe.tags.add(sample_tag(user=self.user))
		recipe.ingrediants.add(sample_ingrediant(user=self.user))
		
		url = detail_url(recipe.id)
		result = self.client.get(url)
		
		serializer = RecipeDetailSerializer(recipe)
		self.assertEqual(result.data, serializer.data)
		
		
		