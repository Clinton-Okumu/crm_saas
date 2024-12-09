# hrm/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, EmployeeViewSet, SalaryViewSet, LeaveViewSet

# Create a router and register your viewsets
router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'salaries', SalaryViewSet, basename='salary')
router.register(r'leave-requests', LeaveViewSet, basename='leave')

# Include the router's URLs in the urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # Automatically includes all the routes registered by the router
]

