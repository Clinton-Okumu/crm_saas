from rest_framework import serializers
from .models import Customer, Contact, Interaction

class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contact model.
    
    Handles the serialization and deserialization of Contact instances,
    including validation of contact information.
    """
    
    # Add a custom field to display the full name
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Contact
        fields = [
            'id',
            'customer',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone',
            'position',
            'is_primary',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
        
    def get_full_name(self, obj):
        """
        Get the contact's full name.
        
        Args:
            obj: Contact instance
            
        Returns:
            str: The contact's full name
        """
        return f"{obj.first_name} {obj.last_name}"
    
    def validate_email(self, value):
        """
        Validate the email field.
        
        Args:
            value: The email to validate
            
        Returns:
            str: The validated email
            
        Raises:
            serializers.ValidationError: If email is invalid
        """
        if value and not "@" in value:
            raise serializers.ValidationError("Please provide a valid email address")
        return value

class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model.
    
    Includes basic customer information and optionally includes
    related contacts when requested.
    """
    
    # Nested serializer for contacts - will be included when specified
    contacts = ContactSerializer(many=True, read_only=True, required=False)
    
    class Meta:
        model = Customer
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'website',
            'address',
            'status',
            'contacts',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class InteractionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Interaction model.
    
    Handles interaction records with related customer and contact information.
    """
    
    # Add custom fields to show related names
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    contact_name = serializers.SerializerMethodField()
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Interaction
        fields = [
            'id',
            'customer',
            'customer_name',
            'contact',
            'contact_name',
            'type',
            'notes',
            'date',
            'created_at',
            'created_by',
            'created_by_username'
        ]
        read_only_fields = ['created_at', 'created_by']

    def get_contact_name(self, obj):
        """
        Get the contact's full name if a contact exists.
        
        Args:
            obj: Interaction instance
            
        Returns:
            str: Contact's full name or None
        """
        if obj.contact:
            return f"{obj.contact.first_name} {obj.contact.last_name}"
        return None
