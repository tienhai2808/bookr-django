from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from reviews.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
  serializer_class = CustomTokenObtainPairSerializer
  
  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    tokens = serializer.validated_data
    response_data = {'access': tokens['access'], 'refresh': tokens['refresh'], 'user': tokens['user']}
    return Response(response_data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [permissions.AllowAny]


class PublisherViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Publisher.objects.all()
  serializer_class = PublisherSerializer
  permission_classes = [permissions.AllowAny]
  
  
class BookViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Book.objects.all()
  serializer_class = BookForPublisherSerializer
  permission_classes = [permissions.AllowAny]
  lookup_field = 'slug'
  
  def get_queryset(self):
    q = self.request.query_params.get('q', '')
    if q:
      return Book.objects.filter(title__icontains=q)
    else:
      return Book.objects.all()
    
    
class ContributorViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Contributor.objects.all()
  serializer_class = ContributorSerializer
  permission_classes = [permissions.AllowAny]
  
  
class ReviewViewSet(viewsets.ModelViewSet):
  queryset = Review.objects.order_by('-date_created')
  serializer_class = ReviewForBookSerializer
  permission_classes = [permissions.AllowAny]
  



