from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, DocumentViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'documents', DocumentViewSet, basename='document')

urlpatterns = router.urls
