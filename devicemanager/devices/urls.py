from rest_framework.routers import DefaultRouter
from .views import FPGAViewSet

router = DefaultRouter()
router.register(r'fpgas', FPGAViewSet)

urlpatterns = router.urls
