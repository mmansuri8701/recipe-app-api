from rest_framework import viewsets, mixins

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingrediant, Recipe
from recipe import serializers

class BaseRecipeAttrViewSet(viewsets.GenericViewSet, 
							mixins.ListModelMixin,
							mixins.CreateModelMixin):
	"""Base view set for user owned recipes"""
	authentication_class = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	
	def get_queryset(self):
		"""Return objects for current authenticated user"""
		return self.queryset.filter(user=self.request.user).order_by('-name')
		
	def perform_create(self, serializer):
		"""Create a new object"""
		serializer.save(user=self.request.user)

class TagViewSet(BaseRecipeAttrViewSet):
	"""Manage tags in the database"""
	queryset = Tag.objects.all()
	serializer_class = serializers.TagSerializer
		
class IngrediantViewSet(BaseRecipeAttrViewSet):
	"""Manage ingrediant in the database """
	queryset = Ingrediant.objects.all()
	serializer_class = serializers.IngrediantSerializer

class RecipeViewSet(viewsets.ModelViewSet):

	"""Manage recipes in the database"""
	serializer_class = serializers.RecipeSerializer
	queryset = Recipe.objects.all()
	authentication_class = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	
	def get_queryset(self):
		"""Retrieve the recipes for the authenticated user"""
		return self.queryset.filter(user=self.request
		.user)
	
	def get_serializer_class(self):
		"""Return appropriate serializer class"""
		if self.action == 'retrieve':
			return serializers.RecipeDetailSerializer
		
		return self.serializer_class
	