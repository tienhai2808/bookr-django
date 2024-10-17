from django.urls import path
from .views import *

urlpatterns = [
  path('', index, name='home'),
  path('book-search/', search, name='search' ),
  path('books/', book_list, name='book-list'),
  path('books/<int:int>/', book_detail, name='book-detail'),
  # path('form-example/', form_example, name = 'form-example'),
  path("publishers/<int:pk>/", publisher_edit, name="publisher-edit"),
  path("publishers/new/", publisher_edit, name="publisher-create"),
  path('books/<int:book_pk>/reviews/<int:review_pk>/', review_edit, name='review-edit'),
  path('books/<int:book_pk>/reviews/new/', review_edit, name='review-create')
]

