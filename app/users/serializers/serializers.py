"""Serializers for the users app."""
from rest_framework.serializers import ModelSerializer

from users.models import User

class UserSerializer(ModelSerializer):
    """User serializer."""
    class Meta:
        """Meta class."""
        model = User
        fields = ('uuid', 'name', 'document', 'created_at', 'updated_at',)
        read_only_fields = ('created_at', 'updated_at', 'uuid',)
