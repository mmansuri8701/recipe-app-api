from unittest.mock import patch
from core import simple

from django.test import TestCase

class SimpleTest(TestCase):
		
	def test_use_simple_function(self):
		#result = simple.simple_function()
		print(simple.simple_function())