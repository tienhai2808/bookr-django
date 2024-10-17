from django.contrib import admin
from .models import Book, Contributor, Review, BookContributor, Publisher
from django.contrib.auth.models import User, Group
# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
  exclude = ('date_edited',)
  # fields = ('content', 'rating', 'creator', 'book')
  fieldsets = (
    (None, {"fields": ("creator", "book")}),
    ("Review content", {"fields": ("content", "rating")}),
  )

class BookAdmin(admin.ModelAdmin):
  search_fields = ('title', 'isbn')
  date_hierarchy = 'publication_date'
  list_display = ('title', 'isbn13', 'publisher', 'has_isbn')
  list_filter = ('publisher', 'publication_date')

  @admin.display(ordering='isbn', description='ISBN-13', empty_value='-/-')
  def isbn13(self, obj):
    return "{}-{}-{}-{}-{}".format(obj.isbn[0:3], obj.isbn[3:4], obj.isbn[4:6], obj.isbn[6:12], obj.isbn[12:13])

  @admin.display(boolean=True, description='Has ISBN', )
  def has_isbn(self, obj):
    return bool(obj.isbn)
  
class ContributorAdmin(admin.ModelAdmin):
  list_display = ('first_names', 'last_names')
  ordering = ('first_names', 'last_names')
  list_filter = ('last_names',)
  search_fields = ('first_names', 'last_names')


admin.site.register(Book, BookAdmin)
admin.site.register(BookContributor)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Publisher)
admin.site.register(Review, ReviewAdmin)
