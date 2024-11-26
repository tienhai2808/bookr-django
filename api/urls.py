from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'publishers', PublisherViewSet, basename='publishers-api')
router.register(r'contributors', ContributorViewSet, basename='contributors-api')
router.register(r'books', BookViewSet, basename='books-api')
router.register(r'reviews', ReviewViewSet, basename='reviews-api'),
router.register(r'users', UserViewSet, basename='users-api')
 
urlpatterns = [
  path("login/", CustomTokenObtainPairView.as_view(), name="login"),
  path("refresh/", TokenRefreshView.as_view(), name="refresh"),
  path("auth/", include("rest_framework.urls")),
] + router.urls