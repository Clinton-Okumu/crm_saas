from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Document
from .serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing Document resources.
    Provides standard CRUD functionality and custom actions for sharing.
    """

    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Returns documents owned by or shared with the current user.
        """
        user = self.request.user
        return Document.objects.filter(
            Q(created_by=user) | Q(shared_with=user)
        ).distinct()

    def perform_create(self, serializer):
        """
        Automatically sets the creator of the document to the current user.
        """
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        """
        Custom action to share a document with another user.
        """
        document = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = settings.AUTH_USER_MODEL.objects.get(id=user_id)
            document.shared_with.add(user)
            return Response({"message": "Document shared successfully."}, status=status.HTTP_200_OK)
        except settings.AUTH_USER_MODEL.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)

