
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer
from .permissions import IsOwnerOrReadOnly

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Optionally filters the queryset based on search query and public status.
        """
        queryset = Document.objects.all()
        search = self.request.query_params.get('search', '')
        is_public = self.request.query_params.get('is_public', None)

        if search:
            queryset = queryset.filter(title__icontains=search)

        if is_public is not None:
            queryset = queryset.filter(is_public=is_public)

        return queryset

    def perform_create(self, serializer):
        """Set the user who created the document."""
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_public(self, request, pk=None):
        """
        Toggle the document's public status.
        """
        document = self.get_object()
        document.is_public = not document.is_public
        document.save()
        return Response({'status': 'Document visibility updated', 'is_public': document.is_public})
