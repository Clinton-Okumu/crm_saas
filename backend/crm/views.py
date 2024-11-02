from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer, Contact, Interaction
from .serializers import CustomerSerializer, ContactSerializer, InteractionSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing customer data.
    
    Provides CRUD operations for customers and includes filtering, searching,
    and custom actions for related data.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['-created_at']

    @action(detail=True, methods=['get'])
    def contacts(self, request, pk=None):
        """
        Retrieve all contacts for a specific customer.
        
        Args:
            request: HTTP request object
            pk: Primary key of the customer
            
        Returns:
            Response: List of contacts for the customer
        """
        customer = self.get_object()
        contacts = Contact.objects.filter(customer=customer)
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def interactions(self, request, pk=None):
        """
        Retrieve all interactions for a specific customer.
        
        Args:
            request: HTTP request object
            pk: Primary key of the customer
            
        Returns:
            Response: List of interactions for the customer
        """
        customer = self.get_object()
        interactions = Interaction.objects.filter(customer=customer)
        serializer = InteractionSerializer(interactions, many=True)
        return Response(serializer.data)

class ContactViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing contact data.
    
    Provides CRUD operations for contacts with filtering and searching capabilities.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['customer', 'is_primary']
    search_fields = ['first_name', 'last_name', 'email', 'position']
    ordering_fields = ['last_name', 'created_at']
    ordering = ['last_name']

    @action(detail=True, methods=['post'])
    def set_primary(self, request, pk=None):
        """
        Set a contact as the primary contact for their customer.
        
        Args:
            request: HTTP request object
            pk: Primary key of the contact
            
        Returns:
            Response: Updated contact data
        """
        contact = self.get_object()
        # Reset any existing primary contacts for this customer
        Contact.objects.filter(customer=contact.customer, is_primary=True).update(is_primary=False)
        contact.is_primary = True
        contact.save()
        serializer = self.get_serializer(contact)
        return Response(serializer.data)

class InteractionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing interaction data.
    
    Provides CRUD operations for interactions with filtering and custom actions.
    """
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['customer', 'contact', 'type']
    search_fields = ['notes']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']

    def perform_create(self, serializer):
        """
        Create a new interaction and set the created_by field.
        
        Args:
            serializer: Interaction serializer instance
        """
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Get recent interactions across all customers.
        
        Args:
            request: HTTP request object
            
        Returns:
            Response: List of recent interactions
        """
        recent_interactions = Interaction.objects.order_by('-date')[:10]
        serializer = self.get_serializer(recent_interactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """
        Get interaction counts grouped by type.
        
        Args:
            request: HTTP request object
            
        Returns:
            Response: Dictionary of interaction counts by type
        """
        from django.db.models import Count
        type_counts = (
            Interaction.objects.values('type')
            .annotate(count=Count('id'))
            .order_by('type')
        )
        return Response(type_counts)

