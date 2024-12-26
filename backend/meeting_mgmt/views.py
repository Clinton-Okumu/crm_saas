from rest_framework import generics
from .models import Meeting
from .serializers import MeetingSerializer

# List all meetings or create a new meeting
class MeetingListCreateView(generics.ListCreateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

# Retrieve, update, or delete a specific meeting
class MeetingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
