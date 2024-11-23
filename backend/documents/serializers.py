from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Document model, including metadata like file size and type.
    """

    file_size = serializers.SerializerMethodField()
    file_type = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ('slug', 'created_by')

    def get_file_size(self, obj):
        """
        Returns a human-readable file size.
        """
        if not obj.file:
            return None
        size = obj.file.size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def get_file_type(self, obj):
        """
        Returns the file extension.
        """
        return obj.file.name.split('.')[-1].upper() if obj.file else None

