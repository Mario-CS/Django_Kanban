from rest_framework.routers import DefaultRouter
from .api_views import BoardViewSet, ColumnViewSet, CardViewSet

router = DefaultRouter()
router.register(r'boards', BoardViewSet, basename='board')
router.register(r'columns', ColumnViewSet, basename='column')
router.register(r'cards', CardViewSet, basename='card')

urlpatterns = router.urls
