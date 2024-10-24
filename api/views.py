from django.contrib.auth import authenticate
from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView
from reviews.models import Book, Review, Publisher
from .serializers import BookSerializer, ReviewSerializer, PublisherSerializer

  

class PublisherViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Publisher.objects.all()
  serializer_class = PublisherSerializer
  permission_classes = [permissions.AllowAny]
  
  
  
class BookViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [permissions.AllowAny]
  
  
class ReviewViewSet(viewsets.ModelViewSet):
  queryset = Review.objects.order_by('-date_created')
  serializer_class = ReviewSerializer
  permission_classes = [permissions.AllowAny]



