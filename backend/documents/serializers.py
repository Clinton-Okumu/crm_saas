from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'description', 'file', 'status', 'is_public', 'created_by', 'created_at', 'updated_at']
