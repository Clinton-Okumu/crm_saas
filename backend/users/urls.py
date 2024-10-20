from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProfileView

#Creating a ruter to route UserviewSet endpoints
router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Include the router-generated routes for users
    path('profile/', UserProfileView.as_view(), name='user-profile'),  # URL for profile view
]