"""
Views for the recipie APIs
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipie
from recipie import serializers


class RecipieViewSet(viewsets.ModelViewSet):
    """View for manage recipie APIs"""

    serializers_class = serializers.RecipieSerializer
    queryset = Recipie.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipies for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')
