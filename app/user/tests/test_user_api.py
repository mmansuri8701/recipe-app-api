"""URLS Revers package is used to get the URL by giving the internal URL mapping"""
from django.urls import reverse
"""Get user model is the auth module function for creating the new user in the system"""
from django.contrib.auth import get_user_model
"""Test case package for Testing the module..."""
from django.test import TestCase
"""Rest framework test module and APIClient function to make HTTP post call with the URL""" 
from rest_framework.test import APIClient
"""Status function used to check the response received from the HTTP request"""
from rest_framework import status

"""Create the hard coded URL from the defined URL mapping"""
CREATE_USER_URL = reverse('user:create')

TOKEN_URL = reverse('user:token')

'''Helper function'''
"""Here **params is object that is passed as input. This will be forwarded to the create user api which will create the user. Mandatory field for the params is the email, password"""
def create_user(**params):
	return get_user_model().objects.create_user(**params)
	
	

class PublicUserApiTests(TestCase):
	"""Test the users API public"""
	def setUp(self):
		"""Client variable is used to fire HTTP post request"""
		self.client = APIClient()
	
	def test_create_valid_user_success(self):
		"""Test creating user with valid payload is successful"""
		"""Sample payload structure to be recevied in HTTP call"""
		payload = {
			'email': 'test@test.com',
			'password': 'testpass',
			'name' : 'Test name'
		}
		"""Fire POST call with input payload"""
		result = self.client.post(CREATE_USER_URL, payload)
		
		"""Check if the status of the HTTP call is success or not"""
		self.assertEqual(result.status_code, status.HTTP_201_CREATED)
		
		"""Extract the result data"""
		user = get_user_model().objects.get(**result.data)
		
		"""Check the password is correct or not"""
		self.assertTrue(user.check_password(payload['password']))
		
		"""Check the result data does not contain the password"""
		self.assertNotIn('password',result)
	
	def test_user_exists(self):
		"""Test creating a user that already exists fails"""
		"""Sample payload structure to be recevied in HTTP call"""
		payload = {'email': 'test@test.com', 'password':'testpass'}
		
		"""Create user with the payload"""
		create_user(**payload)
		
		"""Fire POST call with input payload. Here we are creating a already existing user by firing the POST call.."""
		result = self.client.post(CREATE_USER_URL, payload)
		
		"""Fire POST call with input payload. The result should fail..."""
		self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
		
		
	def test_password_too_short(self):
		"""Test that the password must be more than 5 characters"""
		payload = {"email": "test@test.com", "password": "pw"}
		
		"""Fire HTTP Post call to create user with above payload"""
		result = self.client.post(CREATE_USER_URL, payload)
		
		
		"""The test must fail as the user password is less than 5 characters..."""
		self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
		user_exists = get_user_model().objects.filter(
			email = payload['email']
		).exists()
		
		"""The user must not exists in the system as the password is too short..."""
		self.assertFalse(user_exists)

	
	def test_create_token_for_user(self):
		"""Test that a token is created for the user"""
		payload = {'email' : 'test@test.com', 'password': 'testpass'}
		create_user(**payload)
		result = self.client.post(TOKEN_URL, payload)
		
		self.assertIn('token', result.data)
		self.assertEqual(result.status_code, status.HTTP_200_OK)
		
	def test_create_token_invalid_credentials(self):
		"""Test that token is not created if invalid credentials are given"""
		create_user(email='test@test.com', password= 'testpass')
		payload = {'email': 'test@test.com', 'password': 'wrong'}
		
		result = self.client.post(TOKEN_URL, payload)
		
		self.assertNotIn('token',result.data)
		self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
		
	def test_create_token_no_user(self):
		"""Test that token is not created if user does not exists"""
		payload = {'email': 'test@test.com', 'password': 'wrong'}
		result = self.client.post(TOKEN_URL, payload)
		
		self.assertNotIn('token', result.data)
		self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
		
	def test_create_token_missing_field(self):
		"""Test that email and password are required"""
		
		result = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
		self.assertNotIn('token', result.data)
		self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)