from rest_framework import viewsets, mixins

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingrediant
from recipe import serializers

class TagViewSet(viewsets.GenericViewSet, 
				mixins.ListModelMixin,
				mixins.CreateModelMixin):
	"""Manage tags in the database"""
	authentication_class = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	queryset = Tag.objects.all()
	serializer_class = serializers.TagSerializer
	
	def get_queryset(self):
		"""Return objects for the current authenticated user only"""
		return self.queryset.filter(user=self.request.user).order_by('-name')
	
	def perform_create(self, serializer):
		"""Create a new tag"""
		serializer.save(user=self.request.user)
		
class IngrediantViewSet(viewsets.GenericViewSet, 
						mixins.ListModelMixin):
	"""Manage ingrediant in the database """
	authentication_class = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	queryset = Ingrediant.objects.all()
	serializer_class = serializers.IngrediantSerializer
	
	def get_queryset(self):
		"""Return objects for the current authenticated user only"""
		return self.queryset.filter(user=self.request.user).order_by('-name')
		