from django.urls import path, include
from .views import *
from .api_views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'reviews', ReviewViewSet)


urlpatterns = [
  path('', index, name='home'),
  path('book-search/', search, name='search'),
  path('books/', book_list, name='book-list'),
  path('books/<int:int>/', book_detail, name='book-detail'),
  path("publishers/<int:pk>/", publisher_edit, name="publisher-edit"),
  path("publishers/new/", publisher_edit, name="publisher-create"),
  path('books/<int:book_pk>/reviews/<int:review_pk>/', review_edit, name='review-edit'),
  path('books/<int:book_pk>/reviews/new/', review_edit, name='review-create'),
  path('api/', include((router.urls, 'api'))),
  path('api/login/', Login.as_view(), name='login')
]

