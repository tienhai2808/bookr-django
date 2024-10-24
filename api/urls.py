from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'books', BookViewSet, basename='books-api')
router.register(r'publishers', PublisherViewSet, basename='publishers-api')
router.register(r'reviews', ReviewViewSet, basename='reviews-api')


urlpatterns = router.urls