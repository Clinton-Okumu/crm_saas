from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ObjectiveViewSet, KeyResultViewSet, TaskViewSet


router = DefaultRouter()

router.register = (r'objectives', ObjectiveViewSet)
router.register = (r'keyresults', KeyResultViewSet)
router.register = (r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
