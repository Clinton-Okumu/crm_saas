from django.urls import path
from .views import MeetingListCreateView, MeetingRetrieveUpdateDestroyView

urlpatterns = [
    path('meetings/', MeetingListCreateView.as_view(), name='meeting-list-create'),
    path('meetings/<int:pk>/', MeetingRetrieveUpdateDestroyView.as_view(), name='meeting-retrieve-update-destroy'),
]
