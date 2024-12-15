from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from reviews.models import *
from reviews.utils import average_rating
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
  
  @classmethod
  def get_token(cls, user):
    token = super().get_token(user)
    token['user'] = {'id': user.id, 'username': user.username}
    return token
  
  def validate(self, attrs):
    data = super().validate(attrs)
    data['user'] = {'id': self.user.id, 'username': self.user.username}
    return data
    
    
class UserSerializer(serializers.ModelSerializer):
  old_password = serializers.CharField(write_only=True, required=False)
  reviewed = serializers.SerializerMethodField()
  
  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'reviewed', 'old_password']
    extra_kwargs = {"password": {"write_only": True, "style": {"input_type": "password"}, "required": False}, 
                    "old_password": {"style": {"input_type": "mail"}}}
    
  def get_reviewed(self, user):
    reviews = user.review_set.all()
    return ReviewForUserSerializer(reviews, many=True).data
    
  def create(self, validated_data):
    return User.objects.create_user(**validated_data)
  
  def update(self, instance, validated_data):
    if 'password' in validated_data and 'old_password' in validated_data:
      old_password = validated_data.pop('old_password')
      if not instance.check_password(old_password):
        raise serializers.ValidationError({"Mật khẩu cũ không đúng."})
      else:
        password = validated_data.pop('password')
        instance.set_password(password)
    elif 'password' in validated_data or 'old_password' in validated_data:
      raise serializers.ValidationError({"Nhập mật khẩu vào"})
    return super(UserSerializer, self).update(instance, validated_data)
  

class BookForReviewSerializer(serializers.ModelSerializer):
  class Meta:
    model = Book
    fields = ['title', 'slug']


class ReviewForUserSerializer(serializers.ModelSerializer):
  book = BookForReviewSerializer(read_only=True)
  
  class Meta:
    model = Review
    fields = ['id', 'content', 'date_created', 'rating', 'book']


class PublisherSerializer(serializers.ModelSerializer):  
  books = serializers.SerializerMethodField()
  
  class Meta:
    model = Publisher
    fields = ['id', 'name', 'website', 'email', 'books']
    
  def get_books(self, publisher):
    books = publisher.book_set.all()
    return BookForPublisherSerializer(books, many=True).data


class ContributorSerializer(serializers.ModelSerializer):
  book = serializers.StringRelatedField(read_only=True)
  
  class Meta:
    model = Contributor
    fields = '__all__'
    
    
class BookContributorSerializer(serializers.ModelSerializer):
  contributor = ContributorSerializer(read_only=True)
  
  class Meta:
    model = BookContributor
    fields = ['role', 'contributor', 'book']
  
    
class ReviewForBookSerializer(serializers.ModelSerializer):
  creator = serializers.StringRelatedField(read_only=True)
  
  class Meta:
    model = Review
    fields = ['id', 'content', 'date_created', 'rating', 'creator']
    
  def create(self, validated_data):
    request = self.context["request"]
    book_id = request.data['book_id']
    book = Book.objects.get(id=book_id)
    return Review.objects.create(content=validated_data['content'], book=book, creator=request.user, rating=validated_data['rating'])

  
class BookForPublisherSerializer(serializers.ModelSerializer):
  publisher = serializers.StringRelatedField(read_only=True)
  rating = serializers.SerializerMethodField()
  reviews = serializers.SerializerMethodField()
  contributors = serializers.SerializerMethodField()
  
  class Meta:
    model = Book
    fields = ['id', 'title', 'slug','publication_date', 'cover', 'isbn', 'publisher', 'rating', 'reviews', 'contributors']
      
  def get_rating(self, book):
    reviews = book.review_set.all()
    if reviews:
      return average_rating([review.rating for review in reviews])
    else:
      None
      
  def get_reviews(self, book):
    reviews = book.review_set.all()
    return ReviewForBookSerializer(reviews, many=True).data
      
  def get_contributors(self, book):
    contributors = book.bookcontributor_set.all()
    return BookContributorSerializer(contributors, many=True).data