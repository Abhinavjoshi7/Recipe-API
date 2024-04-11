"""
Serializers for recipie APIs.
"""

from rest_framework import serializers

from core.models import Recipie

class RecipieSerializer(serializers.ModelSerializer):
    """Serializer for recipies."""

    class Meta:
        model = Recipie
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']
