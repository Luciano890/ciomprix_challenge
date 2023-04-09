"""Serializers for the tasks app."""
from rest_framework.serializers import ModelSerializer

from tasks.models import Task

class TaskSerializer(ModelSerializer):
    """Serializer for the Task model."""
    class Meta:
        model = Task
        fields = ('uuid', 'title', 'description', 'end_date', 'created_at', 'updated_at',)
        read_only_fields = ('created_at', 'updated_at', 'uuid',)
