from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, ContactViewSet, InteractionViewSet

# Initialize the router
router = DefaultRouter()

# Register the viewsets with the router
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'interactions', InteractionViewSet, basename='interaction')

# Include the router's URLs in urlpatterns
urlpatterns = [
    path('', include(router.urls)),
]
