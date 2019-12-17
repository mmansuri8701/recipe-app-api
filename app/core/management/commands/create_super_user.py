from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
## Super User name as follows:
## Username: super_user@admin.com
## Password: superuser

class Command(BaseCommand):
	help = 'Custom command to create super user.'
	
	def add_arguments(self, parser):
		parser.add_argument('--username', type=str, help='Username: Email is configured as username')
		parser.add_argument('--password', type=str, help='Password: Mandatory password for the username')
	
	def handle(self, *args, **kwargs):
	
		username = kwargs['username']
		password = kwargs['password']
		self.stdout.write("Input username: %s" % username)
		self.stdout.write("Input password: %s" % password)
		"""Creating super user"""
		user = get_user_model().objects.create_superuser(username, password)
		self.stdout.write("Super user created successfully")