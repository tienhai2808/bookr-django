from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Contributor, Publisher, Review
from .utils import average_rating
from django.db.models import Sum, Q, Count
from django.contrib import messages
from .forms import  *
from django.contrib import messages
from django.utils import timezone
from io import BytesIO
from PIL import Image
from django.core.files.images import ImageFile
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied 

# Create your views here.

def index(request): 
  title = 'Home'
  return render(request, 'pages/home.html', {'title': title})

def search(request):
  title = 'Book Search'
  search_form = SearchForm(request.GET or None)
  if search_form.is_valid():
    search_text = search_form.cleaned_data['search']
    search_in = search_form.cleaned_data['search_in']
    title = f"Search Results for '{search_text}'"
    if search_in == 'Contributor':
      contributors = Contributor.objects.filter(Q(first_names__icontains=search_text)|Q(last_names__icontains=search_text))
      books = Book.objects.filter(contributor__in=contributors).distinct()
    else:
      books = Book.objects.filter(title__icontains=search_text)
    context = {'title': title, 'search_form': search_form, 'search_text':search_text, 'books': books}
  else:
    context = {'title': title, 'search_form': search_form}
  return render(request,'pages/book-search.html', context)

def book_list(request):
  title = 'All Book'
  books = Book.objects.all()
  for book in books:
    reviews = book.review_set.all()
    if reviews:
      book.book_rating = average_rating([review.rating for review in reviews])
      book.number_of_reviews = len(reviews)
    else:
      book.book_rating = None
      book.number_of_reviews = 0
  return render(request, 'pages/book-list.html', {'books': books, 'title': title})

def book_detail(request, int):
  try:
    book = Book.objects.get(id=int)
  except Book.DoesNotExist:
    book = None
  if book:
    title = f'{book.title}'
    count_review = book.review_set.count()
    total_review = book.review_set.aggregate(total_review=Sum('rating'))['total_review']
    if count_review > 0:
      book.avg_rating = total_review/count_review
    else:
      book.avg_rating = None
  else:
    messages.warning(request, 'Không tìm thấy cuốn sách bạn cần')
    return redirect('/')
  context = {'title': title,
              'book': book}
  return render(request, 'pages/book-detail.html', context)

def publisher_edit(request, pk=None):
  if pk is not None:
    publisher = get_object_or_404(Publisher, pk=pk)
  else:
    publisher = None
  if request.POST:
    form = PublisherForm(request.POST, instance=publisher)
    if form.is_valid():
      updated_publisher = form.save()
    if publisher:
      messages.success(request, f"Publisher '{updated_publisher}' was updated.")
    else:
      messages.success(request, f"Publisher '{updated_publisher}' was created.")
    return redirect("publisher-edit", updated_publisher.pk)
  else:
    if not publisher:
      title = "New Publisher"
    else:
      title = f"Edit Publisher {publisher}"
    form = PublisherForm(instance=publisher)
  return render(request, "pages/instance-form.html", {"method": request.method, "title": title, "model_type": "Publisher" ,"instance": publisher, "form": form})

@login_required 
def review_edit(request, book_pk, review_pk=None):
  try:
    book = Book.objects.get(pk=book_pk)
    if review_pk is not None:
      try:
        review = Review.objects.get(book_id=book_pk, pk=review_pk)
        if not request.user.is_staff and review.creator.id != request.user.id:
          raise PermissionDenied
      except Review.DoesNotExist:
        messages.error(request, 'Không tìm thấy review')
        return redirect('book-list')     
    else:
      review = None
    if request.POST:
      form = ReviewForm(request.POST, instance=review)
      if form.is_valid():
        updated_review = form.save(False)
        updated_review.book = book
        if review is None:
          messages.success(request, f'Review for "{book}" created.')
        else:
          updated_review.date_edited = timezone.now()
          messages.success(request, f'Review for "{book}" updated.')
        updated_review.save()
        return redirect('book-detail', book_pk)
    else:
      if not review:
        title = f"New Review for {book.title}"
      else:
        title = f"Edit Review for {book.title}"
      form = ReviewForm(instance=review)
    return render(request, "pages/instance-form.html",
                  {"method": request.method, "title": title, "related_model_type": "Book", "related_instance": book,
                  "model_type": "Review" ,"instance": review, "form": form})
  except Book.DoesNotExist:
    messages.error(request, 'Không tìm thấy cuốn sách')
    return redirect('book-list')

@login_required 
def book_media(request, id_book):
  try:
    book = Book.objects.get(id=id_book)
    title = f'Edit Book {book}'
    form = BookMediaForm(request.POST or None, request.FILES or None, instance=book)
    if request.POST:
      if form.is_valid():
        book = form.save(False)
        cover = form.cleaned_data.get("cover")
        if cover and not hasattr(cover, "path"):
          image = Image.open(cover)
          image.thumbnail((300, 300))
          image_data = BytesIO() #Tạo luồng bộ nhớ tạm RAM
          image.save(fp=image_data, format=cover.image.format) #Lưu ảnh vào bộ nhớ tạm với đúng đinh dạng ban đầu
          image_file = ImageFile(image_data) #Tạo file ảnh từ bộ nhớ tạm
          book.cover.save(cover.name, image_file) #Lưu vào csdl với tên và lưu file ảnh vào folder media
        book.save()
        messages.success(request, f'Sách "{book}" đã được cập nhật thành công.')
        return redirect('book-detail', book.id)
    return render(request, "pages/instance-form.html", {"instance": book, "form": form, "model_type": "Book", 'title': title, "is_file_upload": True})
  except Book.DoesNotExist:
    return redirect('book-list')

def profile(request):
  title = 'Bookr'
  return render(request, 'pages/profile.html', {'title': title})
