from rest_framework import serializers
from .models import Category, Document, DocumentShare

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'id', 'title', 'description', 'category', 'status',
            'file', 'file_size', 'version', 'is_public',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['file_size', 'version', 'created_at', 'updated_at']

class DocumentShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentShare
        fields = ['id', 'document', 'user', 'permission', 'shared_at']
        read_only_fields = ['shared_at']

# views.py
from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Category, Document, DocumentShare
from .serializers import CategorySerializer, DocumentSerializer, DocumentShareSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(
            Q(created_by=self.request.user) |
            Q(shared_with=self.request.user) |
            Q(is_public=True)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
